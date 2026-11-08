"""
Nexora - Voice Laptop Program (Test Version v6)
================================================
A small Windows program you control with your voice.

- Speak or type a command, and Nexora does it: opens Word /
  Chrome / Notepad / YouTube, searches Google/YouTube, types what
  you dictate, tells the time, changes volume, and more.
- Nexora speaks the WORLD's languages: 60+ recognition languages
  (nexora_languages.py). Nexora listens in the chosen language,
  replies in that same language (localised reply phrases for ~21
  languages, English replies for the rest), and does the work.
  Command words are trained for English, Roman Urdu and ~10 more
  languages (nexora_i18n_commands.py).
- v5 changes (from real user testing of v4):
  * NEW HOME DESIGN: logo header, a strip of 4 picture tiles,
    4 CIRCLE buttons on the LEFT (Voice / Language / Help /
    Floating), and the Type box + conversation log on the RIGHT.
  * The app ALWAYS starts in English. The language only changes
    when the user picks one from the Language circle menu.
  * ALWAYS-LISTEN: tap the 🎤 Voice circle ONCE and Nexora keeps
    listening and doing commands - no clicking again and again.
    Tap it again to stop; it never switches itself off.
  * LOCAL APPS OPEN PROPERLY: a much stronger Windows launch
    layer (curated paths, ShellExecute, PATH, registry App Paths,
    Start Menu + Desktop shortcut scan), new "open desktop" and
    "open my computer / this pc" targets, and generic
    "open <any app name>" lookup.
  * SMARTER PHRASING: polite lead-ins ("nexora please ...",
    "can you ...", "and ...") are understood (nexora_commands.py).
- v6 changes (from real user testing of v5 on a 1366x768 laptop):
  * WINDOW FITS SMALL SCREENS: the window sizes itself from the
    real screen, the header is compact, and the 4 circle buttons
    sit in a compact 2x2 grid - nothing is cut off any more.
  * PHOTOS ARE THE BACKGROUND: the 4 picture tiles now form one
    dimmed background photo (assets/bg_main.png) behind everything;
    the working panels stay solid navy so text is easy to read.
  * TWO-SIDED CONVERSATION: what YOU said appears in the LEFT
    pane, what NEXORA did appears in the RIGHT pane.
  * FULLY LOCALISED SCREEN TEXT: every label, status and message
    comes from the selected language's strings - with English
    selected the screen is pure English (no Roman Urdu anywhere).
  * SHORT + MISHEARD COMMANDS WORK: "desktop", "music",
    "documents", "open C drive", and misheard targets are
    repaired ("destop" -> desktop) by the v6 parser.
  * CALMER MIC: the always-listen loop re-calibrates to the
    room noise at startup and after repeated failures.
- The parser is accuracy-first: a command fires only when it is
  the main intent of the sentence (see nexora_commands.py and
  test_accuracy.py). Parsers live in nexora_commands.py (v1) and
  nexora_i18n_commands.py (v2 multilingual matcher).

Optional libraries (program still runs without them, only that
feature is off and Nexora tells you):
    SpeechRecognition  -> listening to your voice (needs PyAudio)
    pyttsx3            -> speaking back to you
    pyautogui          -> pasting dictated text, volume keys, Alt+F4
    pyperclip          -> clipboard for dictation

Every action fails gracefully: a friendly message is spoken/logged,
the program never crashes on a failed action.
"""

import datetime
import os
import re
import shutil
import subprocess
import sys
import threading
import urllib.parse
import webbrowser

from nexora_commands import parse_command

# v2 modules - guarded too: if they are somehow missing, Nexora falls
# back to v1 English/Urdu behaviour instead of crashing.
try:
    from nexora_i18n_commands import parse_command_v2
except Exception:
    parse_command_v2 = None

try:
    from nexora_languages import (
        LANGUAGES,
        code_from_display,
        get_replies,
        locale_display_names,
    )
except Exception:
    LANGUAGES = [("English (US)", "en-US"), ("Urdu (Pakistan)", "ur-PK")]
    code_from_display = None
    get_replies = None
    locale_display_names = None

# v5: Nexora ALWAYS starts in English. The listening language only
# changes when the user picks one from the Language menu - it is
# never auto-detected from the country/system and never restored
# from a previous session.
DEFAULT_LOCALE = "en-US"

_FALLBACK_REPLIES = {
    "opening": "Opening {target}.",
    "searching": "Searching for {query}.",
    "typing": "Typing: {text}",
    "not_understood": "Sorry, I did not understand that command. Try saying 'open YouTube' or 'search for cats'.",
    "greeting": "Hello! I am Nexora. What can I do for you?",
    "time_intro": "The time is {value}.",
    "date_intro": "Today's date is {value}.",
    # v6 GUI text keys (mirror of nexora_languages English UI set)
    "subtitle": "Speak \u2014 and it gets done",
    "you_said": "You said:",
    "nexora_did": "Nexora:",
    "not_found": "'{name}' was not found on this laptop, so nothing was opened. Please check the name and try again.",
    "listening_on": "Listening is ON \u2014 just speak.",
    "listening_off": "Listening is OFF.",
    "ready_status": "Ready",
    "mic_error": "The microphone could not be heard \u2014 please check the mic and your internet.",
    "examples_line": "Examples: open Word \u2022 open YouTube \u2022 search for cats \u2022 type my name is Ahmad \u2022 tell the time",
    "speak_back_label": "Speak back (voice reply)",
}


def replies_for(locale):
    """Localised reply templates for a locale (English fallback)."""
    if get_replies is not None:
        try:
            return get_replies(locale)
        except Exception:
            pass
    return _FALLBACK_REPLIES


def parse_any(text):
    """v2 parser when available, else the v1 parser."""
    if parse_command_v2 is not None:
        try:
            return parse_command_v2(text)
        except Exception:
            pass
    return parse_command(text)


# Display names used in the localised "Opening X." replies
TARGET_NAMES = {
    "open_word": "Microsoft Word",
    "open_chrome": "Google Chrome",
    "open_notepad": "Notepad",
    "open_calculator": "Calculator",
    "open_paint": "Paint",
    "open_explorer": "File Explorer",
    "open_pictures": "Photos",
    "open_videos": "Videos",
    "open_downloads": "Downloads",
    "open_youtube": "YouTube",
    "open_google": "Google",
    "open_desktop": "Desktop",
    "open_this_pc": "This PC",
    "open_documents": "Documents",
    "open_music": "Music",
}

# ---------------------------------------------------------------------------
# Optional libraries - each import is guarded so nothing crashes if missing.
# ---------------------------------------------------------------------------
try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pyperclip
except Exception:
    pyperclip = None

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
except Exception:  # pragma: no cover - tkinter ships with Windows Python
    tk = None

IS_WINDOWS = os.name == "nt"
APP_NAME = "Nexora"
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(name):
    """Absolute path to a bundled resource file (e.g. the logo).

    When Nexora runs frozen as a PyInstaller .exe, bundled data files
    live in the temporary folder pointed to by sys._MEIPASS; when it
    runs as a plain script they sit next to nexora.py. Any failure
    falls back to the script folder, so this can never crash startup.
    """
    try:
        base = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base = APP_DIR
    return os.path.join(base, name)


LOGO_PNG = resource_path("logo-new.png")

TILE_FILES = ("tile_voice.png", "tile_apps.png", "tile_search.png",
              "tile_languages.png")

# ---------------------------------------------------------------------------
# Help text - teaches the user how Nexora works (Help button + popup).
# Pure simple English - the app screen never shows Roman Urdu.
# ---------------------------------------------------------------------------
HELP_TEXT = """WHAT IS NEXORA?
Nexora is a small program for your Windows laptop.
You speak, and Nexora does the work - it opens programs,
searches the internet, types for you, and more.
Nexora also speaks back to you and tells you what it did.

IMPORTANT - NEXORA IS ONLINE
Voice works online - internet must be ON.
Nexora listens to your voice through the internet, so keep
your internet connected when you speak.
No internet? You can still TYPE a command. Typed commands for
programs on your laptop (like Notepad or Calculator) can work
offline, but voice, YouTube and search need internet.

LANGUAGE - STARTS IN ENGLISH
Nexora always starts in English, and the whole screen is in
the language you pick. To change the language, tap the
Language circle button and pick your language from the list.
Nexora then listens, replies and shows its screen in that
language.

HOW TO USE NEXORA - ALWAYS-LISTEN
1. Tap the Voice circle button ONE time.
   The ring turns GREEN and Nexora keeps listening.
2. Just speak your commands, one after another - you do
   NOT need to click again for every command.
3. Tap the Voice circle button again to STOP listening.
   Nexora never switches listening off by itself - it
   stays ON until you tap it off.
You can also type a command in the box on the right and
press the tick button - typing always works too.

THE TWO BOXES ON THE RIGHT
The LEFT box shows what YOU said.
The RIGHT box shows what NEXORA did.
So you can always see your words and Nexora's work side
by side.

SHORT COMMANDS ARE ENOUGH
You do not need long perfect sentences. Short commands work:
•  desktop
•  documents
•  music
•  open C drive        (any drive letter works)
•  open Word
•  open YouTube
•  open my computer
•  open Spotify        (any app, by its name)
•  play songs          (plays on YouTube)
•  search Google for cats
•  search YouTube for songs
•  type hello, my name is Ahmad
•  what time is it
•  volume up
Small hearing mistakes are repaired too - if you say
"destop", Nexora understands "desktop".
You can also speak naturally: "Nexora, please open
YouTube" and "can you open Chrome" work too.

TIPS
• Speak slowly and clearly, close to the mic.
• One command at a time.
• If Nexora does not hear you, check your internet and
  your mic, then try again.

FLOATING NEXORA ICON
A small Nexora "N" icon stays on top of every window.
• Drag it anywhere on the screen - it stays where you drop it.
• Tap (click) it to open a mini panel: a Voice button (the
  same always-listen ON/OFF), a text box with a tick button,
  and a Home button that brings the Nexora window forward.
• The icon's ring turns GREEN while Nexora is listening.
• Hide it from the mini panel (Hide icon) and bring it back
  any time with the Floating circle button in the main window.
"""


# ---------------------------------------------------------------------------
# Launch helpers - the strong Windows launch layer (v5, all guarded)
# ---------------------------------------------------------------------------
def _open_folder(path):
    """Open a folder in the file explorer. Returns True/False."""
    try:
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        if IS_WINDOWS:
            os.startfile(path)  # noqa: S606 - user-requested folder
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception:
        return False


def _norm_key(name):
    """'Microsoft Word' -> 'microsoftword' (for name matching)."""
    return re.sub(r"[^a-z0-9]+", "", str(name).lower())


def _office_word_candidates():
    paths = [r"winword"]
    for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                 os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
        for ver in ("Office16", "Office15", "Office14"):
            paths.append(os.path.join(base, "Microsoft Office", "root", ver, "WINWORD.EXE"))
            paths.append(os.path.join(base, "Microsoft Office", ver, "WINWORD.EXE"))
    return paths


def _chrome_candidates():
    paths = [r"chrome"]
    for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                 os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                 os.environ.get("LOCALAPPDATA", "")):
        if base:
            paths.append(os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"))
    return paths


def _curated_paths_for(name):
    """Existing absolute install paths for the well-known apps."""
    key = _norm_key(name)
    builders = {
        "winword": _office_word_candidates,
        "word": _office_word_candidates,
        "microsoftword": _office_word_candidates,
        "msword": _office_word_candidates,
        "chrome": _chrome_candidates,
        "googlechrome": _chrome_candidates,
    }
    builder = builders.get(key)
    if builder is None:
        return []
    return [p for p in builder()
            if os.path.isabs(p) and os.path.isfile(p)]


def _candidate_exes(name):
    """Exe-name variants for a spoken app name."""
    base = str(name).strip()
    variants = []
    for v in (base, base + ".exe",
              base.replace(" ", ""), base.replace(" ", "") + ".exe"):
        if v and v not in variants:
            variants.append(v)
    return variants


def _registry_app_path(exe_name):
    """Look up an exe in the Windows App Paths registry keys (HKLM+HKCU)."""
    try:
        import winreg
    except Exception:
        return None
    subkey = (r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
              + "\\" + exe_name)
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(hive, subkey) as key:
                value, _kind = winreg.QueryValueEx(key, None)
            value = str(value).strip().strip('"')
            if value and os.path.isfile(value):
                return value
        except Exception:
            continue
    return None


def _scan_shortcuts(name):
    """
    Scan the Start Menu Programs folders and the Desktops for a
    shortcut/file whose name matches the app name. Exact normalised
    match wins; otherwise a startswith match. Returns a path or None.
    """
    key = _norm_key(name)
    if not key:
        return None
    roots = []
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        roots.append(os.path.join(
            appdata, "Microsoft", "Windows", "Start Menu", "Programs"))
    roots.append(os.path.join(
        os.environ.get("ProgramData", r"C:\ProgramData"),
        "Microsoft", "Windows", "Start Menu", "Programs"))
    home = os.path.expanduser("~")
    roots.append(os.path.join(home, "Desktop"))
    roots.append(r"C:\Users\Public\Desktop")
    best = None
    for base in roots:
        if not base or not os.path.isdir(base):
            continue
        try:
            for dirpath, _dirs, files in os.walk(base):
                for fname in files:
                    fkey = _norm_key(os.path.splitext(fname)[0])
                    if not fkey:
                        continue
                    if fkey == key:
                        return os.path.join(dirpath, fname)
                    if best is None and len(key) >= 3 and fkey.startswith(key):
                        best = os.path.join(dirpath, fname)
        except Exception:
            continue
    return best


def find_app(name):
    """
    Find a launchable path for an app name on Windows, or None.
    Methods: curated absolute paths -> PATH lookup (shutil.which)
    -> registry App Paths -> Start Menu / Desktop shortcut scan.
    (The bare-name ShellExecute attempt lives in try_launch.)
    """
    if not IS_WINDOWS or not name:
        return None
    for path in _curated_paths_for(name):
        return path
    for variant in _candidate_exes(name):
        found = shutil.which(variant)
        if found:
            return found
    for variant in _candidate_exes(name):
        exe = variant if variant.lower().endswith(".exe") else variant + ".exe"
        path = _registry_app_path(exe)
        if path:
            return path
    return _scan_shortcuts(name)


def _startfile(target):
    """os.startfile, guarded. True when the launch was accepted."""
    try:
        os.startfile(target)  # noqa: S606 - user-requested program
        return True
    except Exception:
        return False


def try_launch(name):
    """
    Try EVERY method to launch an app by name. Returns True/False.
    Order: (a) curated absolute paths, (b) bare name via ShellExecute
    (os.startfile resolves the registry App Paths itself),
    (c) PATH lookup, (d) registry App Paths path, (e/f) Start Menu
    and Desktop shortcut scan.
    """
    if not IS_WINDOWS or not name:
        return False
    for path in _curated_paths_for(name):
        if _startfile(path):
            return True
    for variant in _candidate_exes(name):
        if _startfile(variant):
            return True
    found = find_app(name)
    if found and _startfile(found):
        return True
    return False


def _launch(candidates, friendly_name):
    """
    Launch a known program from a candidate list (exe names or full
    paths) using the strong launch layer. Returns (ok, message).
    """
    if not IS_WINDOWS:
        return False, f"{friendly_name} only opens on Windows - this does not look like a Windows laptop."
    for cand in candidates:
        try:
            if os.path.isabs(cand):
                if os.path.isfile(cand) and _startfile(cand):
                    return True, f"Opening {friendly_name}."
            elif try_launch(cand):
                return True, f"Opening {friendly_name}."
        except Exception:
            continue
    return False, f"{friendly_name} was not found on this laptop. It may not be installed."


# ---------------------------------------------------------------------------
# Action dispatcher - returns a friendly result message, never raises.
# ---------------------------------------------------------------------------
class ActionRunner:
    def __init__(self, app):
        self.app = app  # for scheduling dictation paste on the GUI thread

    def _replies(self):
        locale = "en-US"
        try:
            locale = self.app.language_code()
        except Exception:
            pass
        return replies_for(locale)

    def _opening(self, action):
        return self._replies()["opening"].format(target=TARGET_NAMES.get(action, "it"))

    def run(self, result):
        action = result.get("action", "unknown")
        try:
            return self._run_inner(action, result)
        except Exception as exc:  # absolute safety net
            return f"Something went wrong ({exc}) - please try again."

    def _run_inner(self, action, result):
        if action == "greet":
            return self._replies()["greeting"]

        if action == "open_word":
            ok, msg = _launch(_office_word_candidates(), "Microsoft Word")
            if ok:
                return self._opening(action)
            # Fallback: Word in the browser
            try:
                webbrowser.open("https://www.office.com/launch/word")
                return "Word was not found on this laptop, so I opened the online version of Word in the browser."
            except Exception:
                return msg

        if action == "open_chrome":
            ok, msg = _launch(_chrome_candidates(), "Google Chrome")
            if ok:
                return self._opening(action)
            try:
                webbrowser.open("https://www.google.com")
                return "Chrome was not found, so I opened Google in the default browser."
            except Exception:
                return msg

        if action == "open_notepad":
            ok, msg = _launch(["notepad.exe", "notepad"], "Notepad")
            return self._opening(action) if ok else msg

        if action == "open_calculator":
            ok, msg = _launch(["calc.exe", "calc"], "Calculator")
            return self._opening(action) if ok else msg

        if action == "open_paint":
            ok, msg = _launch(["mspaint.exe", "mspaint", "pbrush.exe"], "Paint")
            return self._opening(action) if ok else msg

        if action == "open_explorer":
            home = os.path.expanduser("~")
            return self._opening(action) if _open_folder(home) else "File Explorer could not be opened."

        if action == "open_pictures":
            path = os.path.join(os.path.expanduser("~"), "Pictures")
            return self._opening(action) if _open_folder(path) else "The Photos folder could not be opened."

        if action == "open_videos":
            path = os.path.join(os.path.expanduser("~"), "Videos")
            return self._opening(action) if _open_folder(path) else "The Videos folder could not be opened."

        if action == "open_downloads":
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            return self._opening(action) if _open_folder(path) else "The Downloads folder could not be opened."

        if action == "open_desktop":
            path = os.path.join(os.path.expanduser("~"), "Desktop")
            return self._opening(action) if _open_folder(path) else "The Desktop folder could not be opened."

        if action == "open_documents":
            path = os.path.join(os.path.expanduser("~"), "Documents")
            return self._opening(action) if _open_folder(path) else "The Documents folder could not be opened."

        if action == "open_music":
            path = os.path.join(os.path.expanduser("~"), "Music")
            return self._opening(action) if _open_folder(path) else "The Music folder could not be opened."

        if action == "open_drive":
            letter = str(result.get("drive") or "C").strip().upper()[:1] or "C"
            if not IS_WINDOWS:
                return f"Drive {letter} can only be opened on a Windows laptop."
            if _startfile(letter + ":\\"):
                return self._replies()["opening"].format(target=f"Drive {letter}")
            return f"Drive {letter} could not be opened."

        if action == "open_this_pc":
            if IS_WINDOWS:
                try:
                    subprocess.Popen(["explorer.exe",
                                      "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"])
                    return self._opening(action)
                except Exception:
                    pass
            home = os.path.expanduser("~")
            return self._opening(action) if _open_folder(home) else "This PC could not be opened."

        if action == "generic_open":
            name = str(result.get("name", "")).strip()
            if not name:
                return self._replies()["not_understood"]
            if try_launch(name):
                return self._replies()["opening"].format(target=name)
            return self._replies()["not_found"].format(name=name)

        if action == "open_youtube":
            webbrowser.open("https://www.youtube.com")
            return self._opening(action)

        if action == "open_google":
            webbrowser.open("https://www.google.com")
            return self._opening(action)

        if action == "google_search":
            query = result.get("query", "").strip()
            if not query:
                webbrowser.open("https://www.google.com")
                return self._opening("open_google")
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))
            return self._replies()["searching"].format(query=query)

        if action == "youtube_search":
            query = result.get("query", "").strip()
            if not query:
                webbrowser.open("https://www.youtube.com")
                return self._opening("open_youtube")
            webbrowser.open("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query))
            return self._replies()["searching"].format(query=query)

        if action == "dictate":
            text = result.get("text", "").strip()
            if not text:
                return "I did not catch what to type - say 'type' followed by your sentence."
            return self.app.schedule_dictation_paste(text)

        if action == "tell_time":
            now = datetime.datetime.now()
            value = now.strftime("%I:%M %p").lstrip("0")
            return self._replies()["time_intro"].format(value=value)

        if action == "tell_date":
            today = datetime.date.today()
            return self._replies()["date_intro"].format(value=today.strftime("%d %B %Y"))

        if action == "close_window":
            return self.app.schedule_close_window()

        if action in ("volume_up", "volume_down", "mute"):
            return self._volume(action)

        return self._replies()["not_understood"]

    def _volume(self, action):
        if pyautogui is None:
            return "Volume cannot be changed right now (the pyautogui library is missing) - please use the keyboard volume keys."
        try:
            if action == "mute":
                pyautogui.press("volumemute")
                return "Muted."
            key = "volumeup" if action == "volume_up" else "volumedown"
            for _ in range(5):
                pyautogui.press(key)
            return "Volume turned up." if action == "volume_up" else "Volume turned down."
        except Exception:
            return "The volume could not be changed."


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
BG = "#0a0e22"           # root / header tone (sits over the photo)
PANEL = "#121935"        # floating mini window
PANEL_BG = "#0d1330"     # solid deep-navy foreground panels (v6)
TEXT_BG = "#0a0f28"      # inset text areas (entry / panes)
CARD = "#1a2342"
RING_OFF = "#38e1ff"     # cyan ring - listening OFF
RING_ON = "#2eff8a"      # bright green ring - listening ON


class NexoraApp:
    def __init__(self, root):
        self.root = root
        self.runner = ActionRunner(self)
        self.tts_engine = None

        # --- listening state (v5 always-listen) ---
        self.always_listening = False
        self._listen_stop = threading.Event()
        self._listen_thread = None
        self._listen_error_logged = False

        root.title("Nexora \u2014 Home (Test v6)")
        # v6: size the window from the REAL screen so nothing is cut
        # off on a 1366x768 laptop (v5's fixed 1180x780 overflowed).
        try:
            screen_w = root.winfo_screenwidth()
            screen_h = root.winfo_screenheight()
        except Exception:
            screen_w, screen_h = 1366, 768
        win_w = min(1180, max(900, screen_w - 16))
        win_h = min(740, max(600, screen_h - 64))
        root.geometry(f"{win_w}x{win_h}")
        root.minsize(900, 600)
        try:
            root.configure(bg=BG)
        except Exception:
            pass
        try:
            root.protocol("WM_DELETE_WINDOW", self.on_close)
        except Exception:
            pass

        # --- Nexora branding images (all guarded) ---
        self._logo_full = None
        self._logo_img = None       # header-size logo
        self._icon_img = None       # window icon image
        self._float_img = None      # floating-icon image
        try:
            if os.path.isfile(LOGO_PNG):
                _full = tk.PhotoImage(file=LOGO_PNG)      # 800x800 source
                self._logo_full = _full
                self._logo_img = _full.subsample(7, 7)    # ~114px header
                self._icon_img = _full.subsample(12, 12)  # ~66px icon
                self._float_img = _full.subsample(12, 12)  # ~66px floating
                try:
                    root.iconphoto(True, self._icon_img)
                except Exception:
                    pass
        except Exception:
            self._logo_full = None
            self._logo_img = None
            self._icon_img = None
            self._float_img = None

        # --- v6 background photo: the 4 tiles as ONE dimmed picture ---
        self._bg_img = None
        try:
            bg_path = resource_path(os.path.join("assets", "bg_main.png"))
            if os.path.isfile(bg_path):
                self._bg_img = tk.PhotoImage(file=bg_path)   # 1280x800
                bg_label = tk.Label(root, image=self._bg_img, bd=0)
                bg_label.place(x=0, y=0)   # behind every other widget
        except Exception:
            self._bg_img = None

        # --- picture tiles kept loaded (v5 strip removed in v6 - the
        # tiles now live inside the background photo above) ---
        self._tile_full = []
        self._tile_imgs = []
        for fname in TILE_FILES:
            try:
                path = resource_path(os.path.join("assets", fname))
                if os.path.isfile(path):
                    _img = tk.PhotoImage(file=path)       # 560x340 source
                    self._tile_full.append(_img)
                    self._tile_imgs.append(_img.subsample(3, 3))  # ~186x113
            except Exception:
                continue

        # Language state must exist before any localised label is made
        self.lang_var = tk.StringVar(value=self._default_display())
        self.speak_var = tk.BooleanVar(value=True)
        _r0 = replies_for(DEFAULT_LOCALE)   # the app always starts English

        # ============ HEADER (centered, compact, over the photo) ====
        # Widgets sit directly on the root so the dimmed background
        # photo shows around them; each label's own bg is the header
        # tone #0A0E22 (BG) so the text stays readable.
        if self._logo_img is not None:
            tk.Label(root, image=self._logo_img, bg=BG).pack(pady=(8, 0))
        tk.Label(root, text="NEXORA", font=("Segoe UI", 24, "bold"),
                 fg="#5b8cff", bg=BG).pack(pady=(2, 0))
        tk.Label(root, text="Speak once \u2014 Nexora does it",
                 font=("Segoe UI", 12, "bold"), fg="#eef1ff", bg=BG).pack()
        self.subtitle_label = tk.Label(
            root, text=_r0["subtitle"], font=("Segoe UI", 11),
            fg="#c6cdf5", bg=BG)
        self.subtitle_label.pack(pady=(0, 2))

        self.status_var = tk.StringVar(value=_r0["ready_status"])
        tk.Label(root, textvariable=self.status_var,
                 font=("Segoe UI", 10, "italic"),
                 fg="#9fd0ff", bg=BG).pack()

        # Speak-back checkbox (top-right corner of the window)
        self.speak_check = None
        try:
            self.speak_check = tk.Checkbutton(
                root, text=_r0["speak_back_label"],
                variable=self.speak_var, bg=BG, fg="#eef1ff",
                activebackground=BG, activeforeground="#eef1ff",
                selectcolor=CARD, font=("Segoe UI", 9))
            self.speak_check.place(relx=1.0, x=-8, y=6, anchor="ne")
        except Exception:
            self.speak_check = None

        # ============ BODY: circles LEFT, type + two panes RIGHT ====
        # The two panels are solid deep-navy (PANEL_BG) so text stays
        # readable; the dimmed photo shows in the gaps around them.
        left = tk.Frame(root, bg=PANEL_BG)
        left.pack(side="left", fill="y", padx=(10, 5), pady=(8, 10))

        self.circle_btns = {}
        self.circle_btns["voice"] = self._make_circle(
            left, "🎤", "Voice: OFF", self.toggle_listening)
        self.circle_btns["language"] = self._make_circle(
            left, "🌐", "Language", self._on_language_circle)
        self.circle_btns["help"] = self._make_circle(
            left, "❓", "Help", self.show_help)
        self.circle_btns["floating"] = self._make_circle(
            left, "🧭", "Floating", self.toggle_floating)
        _grid_pos = {"voice": (0, 0), "language": (0, 1),
                     "help": (1, 0), "floating": (1, 1)}
        for _key, _btn in self.circle_btns.items():
            _r, _c = _grid_pos[_key]
            _btn["canvas"].grid(row=_r, column=_c, padx=3, pady=3)

        right = tk.Frame(root, bg=PANEL_BG)
        right.pack(side="left", fill="both", expand=True, padx=(5, 10),
                   pady=(8, 10))

        # Typed command row (top of the right side)
        row = tk.Frame(right, bg=PANEL_BG)
        row.pack(fill="x", padx=8, pady=(8, 0))
        self.type_label = tk.Label(
            row, text=self._type_label_text(_r0),
            font=("Segoe UI", 12, "bold"), fg="#9fd0ff", bg=PANEL_BG)
        self.type_label.pack(side="left", padx=(0, 6))
        self.entry = tk.Entry(row, font=("Segoe UI", 12), bg=TEXT_BG,
                              fg="#eef1ff", insertbackground="#eef1ff")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.on_do_it())
        tk.Button(row, text="✔", font=("Segoe UI", 12, "bold"),
                  command=self.on_do_it).pack(side="left", padx=(8, 0))

        self.examples_label = tk.Label(
            right, text=_r0["examples_line"], font=("Segoe UI", 9),
            fg="#8f9ac9", bg=PANEL_BG)
        self.examples_label.pack(pady=(4, 0), padx=8, anchor="w")

        # ---- v6 TWO-SIDED conversation: left = you said, right =
        # what Nexora did. Two read-only panes, each autoscrolling.
        panes = tk.Frame(right, bg=PANEL_BG)
        panes.pack(fill="both", expand=True, padx=8, pady=(6, 8))
        panes.columnconfigure(0, weight=1)
        panes.columnconfigure(1, weight=1)
        panes.rowconfigure(1, weight=1)

        self.user_header = tk.Label(
            panes, text=_r0["you_said"], font=("Segoe UI", 10, "bold"),
            fg="#9fd0ff", bg=PANEL_BG, anchor="w")
        self.user_header.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.nexora_header = tk.Label(
            panes, text=_r0["nexora_did"], font=("Segoe UI", 10, "bold"),
            fg="#7dffb0", bg=PANEL_BG, anchor="w")
        self.nexora_header.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.user_text = self._make_pane(panes)
        self.user_text.grid(row=1, column=0, sticky="nsew", padx=(0, 4))
        self.nexora_text = self._make_pane(panes)
        self.nexora_text.grid(row=1, column=1, sticky="nsew", padx=(4, 0))

        self._lang_menu = None

        # ============ startup teaching lines (English - the start
        # language; the screen re-labels itself if the user picks
        # another language) ============
        self.log("👋 Welcome to Nexora v6! This is your Nexora HOME screen - you speak, Nexora does the work.")
        self.log("🎤 ALWAYS-LISTEN: tap the Voice circle button ONE time - Nexora keeps listening, no clicking again for every command. Tap it again to stop; it never switches off by itself.")
        self.log("🗂 The two boxes: the LEFT box shows what YOU said, the RIGHT box shows what NEXORA did.")
        self.log("🌐 Language: Nexora always starts in English. To change it, tap the Language circle button and pick your language - the whole screen changes to it.")
        self.log("🌐 Voice works online — internet must be ON.")
        self.log("Short commands are enough: 'desktop', 'documents', 'music', 'open C drive'. Small hearing mistakes are repaired too.")
        self.log("No mic? Type the command on the right and press ✔. Need help any time? Tap the ❓ Help circle button.")
        self.log(f"🌍 Nexora can listen in {len(LANGUAGES)} languages and replies in the same language (full replies in 21 languages, English for the rest).")
        if sr is None:
            self.log("Note: the 'SpeechRecognition' library was not found - voice listening is off, but typed commands work. Start Nexora with run_nexora.bat and the libraries install themselves.")
        if pyttsx3 is None:
            self.log("Note: the 'pyttsx3' library was not found - Nexora will not speak back, replies will only appear on screen.")
        # Floating Nexora icon (built last, fully guarded)
        self._build_floating()
        if self.float_win is not None:
            self.log("🧭 Floating Nexora icon is ON: it stays on top of every window. Drag it anywhere - tap it for 🎤 Voice (always-listen) or ⌨ text. Its ring turns GREEN while Nexora is listening.")
        self._refresh_listen_ui()

    # ----- language: always starts English, menu changes it -----
    def _lang_values(self):
        if locale_display_names is not None:
            return locale_display_names()
        return [f"{name} ({code})" for name, code in LANGUAGES]

    def _default_display(self):
        """Display label for DEFAULT_LOCALE (en-US) - v5 always-English start."""
        values = self._lang_values()
        for display in values:
            if display.rstrip().endswith(f"({DEFAULT_LOCALE})"):
                return display
        return values[0] if values else "English (US) (en-US)"

    def language_code(self):
        display = self.lang_var.get()
        if code_from_display is not None:
            try:
                return code_from_display(display)
            except Exception:
                pass
        if "(" in display and ")" in display:
            return display[display.rfind("(") + 1:display.rfind(")")].strip()
        return DEFAULT_LOCALE

    def set_language(self, display):
        """Pick a language (session-only). Called from the Language menu."""
        self.lang_var.set(display)
        # Tiny label under the Language circle shows the chosen language
        short = display
        try:
            code = self.language_code()
            for name, lang_code in LANGUAGES:
                if lang_code == code:
                    short = name.split(" ")[0]
                    break
        except Exception:
            pass
        try:
            btn = self.circle_btns.get("language")
            if btn:
                btn["canvas"].itemconfigure(btn["label"], text=short[:12])
        except Exception:
            pass
        # v6: the whole screen re-labels itself in the new language
        self._refresh_localized_labels()
        self.log(f"🌐 Language: {display}")

    def _on_language_circle(self, anchor_widget=None):
        try:
            if self._lang_menu is None:
                menu = tk.Menu(self.root, tearoff=0, bg=PANEL, fg="#eef1ff",
                               activebackground="#2b5cff", activeforeground="white")
                for display in self._lang_values():
                    menu.add_command(
                        label=display,
                        command=lambda d=display: self.set_language(d))
                self._lang_menu = menu
            btn = self.circle_btns.get("language") if anchor_widget is None else None
            widget = anchor_widget or (btn["canvas"] if btn else self.root)
            x = widget.winfo_rootx()
            y = widget.winfo_rooty() + widget.winfo_height()
            self._lang_menu.tk_popup(x, y)
        except Exception:
            pass

    # ----- localised UI text helpers -----
    def ui(self):
        """The current locale's full string set (replies + GUI keys)."""
        return replies_for(self.language_code())

    @staticmethod
    def _type_label_text(replies):
        """
        The label next to the type box, derived from the locale's own
        "typing" template ("Typing: {text}" -> "⌨ Typing:") so it is
        genuinely in the selected language.
        """
        try:
            word = (replies.get("typing", "Typing: {text}")
                    .replace("{text}", "").rstrip(" :\uff1a").strip())
        except Exception:
            word = ""
        return "⌨ " + (word or "Type") + ":"

    def _refresh_localized_labels(self):
        """Re-label the visible static texts in the current language."""
        r = self.ui()
        try:
            self.subtitle_label.configure(text=r["subtitle"])
            self.user_header.configure(text=r["you_said"])
            self.nexora_header.configure(text=r["nexora_did"])
            self.examples_label.configure(text=r["examples_line"])
            self.type_label.configure(text=self._type_label_text(r))
            if self.speak_check is not None:
                self.speak_check.configure(text=r["speak_back_label"])
            if not self.always_listening:
                self.status_var.set(r["ready_status"])
        except Exception:
            pass

    # ----- read-only conversation pane -----
    def _make_pane(self, parent):
        """One pane of the two-sided conversation (text + scrollbar)."""
        frame = tk.Frame(parent, bg=PANEL_BG)
        text = tk.Text(frame, font=("Segoe UI", 10), state="disabled",
                       wrap="word", bg=TEXT_BG, fg="#eef1ff",
                       insertbackground="#eef1ff", relief="flat",
                       padx=6, pady=6)
        text.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(frame, command=text.yview)
        scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll.set)
        frame.text_widget = text
        return frame

    # ----- circular buttons (left panel, compact 2x2 grid in v6) --
    def _make_circle(self, parent, glyph, label, command):
        """
        A circular button drawn on a Canvas (~86px circle): outer
        glow ring, filled circle, a big emoji glyph in the middle
        and a tiny label under it. Returns a dict with the canvas +
        item ids (the Voice button's ring/label are updated by
        _refresh_listen_ui).
        """
        cv = tk.Canvas(parent, width=100, height=116, bg=PANEL_BG,
                       highlightthickness=0, cursor="hand2")
        glow = cv.create_oval(4, 2, 96, 92, outline="#22335f", width=5)
        ring = cv.create_oval(8, 6, 92, 90, fill="#16224a",
                              outline=RING_OFF, width=3)
        glyph_id = cv.create_text(50, 48, text=glyph,
                                  font=("Segoe UI Emoji", 22), fill="#ffffff")
        label_id = cv.create_text(50, 104, text=label,
                                  font=("Segoe UI", 8, "bold"), fill="#c6cdf5")
        cv.bind("<Button-1>", lambda _e: command())
        return {"canvas": cv, "glow": glow, "ring": ring,
                "glyph": glyph_id, "label": label_id}

    # ----- help popup (teaches the user how to use Nexora) -----
    def show_help(self):
        try:
            win = tk.Toplevel(self.root)
            win.title("Nexora — ❓ Help / How to Use")
            win.geometry("600x560")
            win.minsize(420, 380)
            box = scrolledtext.ScrolledText(win, font=("Segoe UI", 11), wrap="word")
            box.pack(padx=12, pady=12, fill="both", expand=True)
            box.insert("end", HELP_TEXT)
            box.configure(state="disabled")
            tk.Button(win, text="Close", font=("Segoe UI", 11, "bold"),
                      command=win.destroy).pack(pady=(0, 12))
        except Exception:
            # If the popup cannot open, teach in the log instead.
            for line in HELP_TEXT.splitlines():
                self.log(line)

    # ----- floating Nexora icon (canvas: ring + status dot mirror listening) -----
    def _build_floating(self):
        """
        Small always-on-top Nexora icon that floats above every other
        window. Drag it anywhere with the mouse; a tap (click without
        dragging) opens a mini panel with a 🎤 Voice toggle, a ⌨ text
        box and a ⌂ Home button. Its ring (and dot) turn GREEN while
        always-listen is ON. Fully guarded - if the floating window
        cannot be created, the main window works without it.
        """
        self.float_win = None
        self.float_panel = None
        self.float_visible = False
        self._float_drag = None
        self._float_canvas = None
        self._float_ring = None
        self._float_dot = None
        self._panel_voice_btn = None
        try:
            win = tk.Toplevel(self.root)
            win.overrideredirect(True)
            try:
                win.attributes("-topmost", True)
            except Exception:
                pass
            try:
                win.configure(bg=BG)
            except Exception:
                pass
            cv = tk.Canvas(win, width=76, height=76, bg=BG,
                           highlightthickness=0, cursor="hand2")
            cv.create_rectangle(6, 6, 70, 70, fill=PANEL, outline="#22335f", width=2)
            self._float_ring = cv.create_oval(5, 5, 71, 71,
                                              outline=RING_OFF, width=3)
            if self._float_img is not None:
                cv.create_image(38, 38, image=self._float_img)
            else:
                cv.create_text(38, 39, text="N", fill="#38e1ff",
                               font=("Segoe UI", 28, "bold"))
            self._float_dot = cv.create_oval(57, 3, 73, 19, fill="#555f7a",
                                             outline="#0b1020", width=2)
            cv.pack()
            self._float_canvas = cv
            # Bind on the canvas only (its bindtags include the
            # Toplevel, so also binding the window would double-fire).
            cv.bind("<ButtonPress-1>", self._float_press)
            cv.bind("<B1-Motion>", self._float_move)
            cv.bind("<ButtonRelease-1>", self._float_release)
            cv.bind("<Button-3>", lambda _e: self.hide_floating())
            try:
                x = max(0, self.root.winfo_screenwidth() - 100)
            except Exception:
                x = 100
            win.geometry(f"+{x}+110")
            self.float_win = win
            self.float_visible = True
        except Exception:
            self.float_win = None
            self.float_visible = False

    def _float_press(self, event):
        if self.float_win is None:
            return
        try:
            self._float_drag = {
                "dx": event.x_root - self.float_win.winfo_x(),
                "dy": event.y_root - self.float_win.winfo_y(),
                "sx": event.x_root, "sy": event.y_root, "moved": False,
            }
        except Exception:
            self._float_drag = None

    def _float_move(self, event):
        if not self._float_drag or self.float_win is None:
            return
        try:
            if (abs(event.x_root - self._float_drag["sx"]) > 4
                    or abs(event.y_root - self._float_drag["sy"]) > 4):
                self._float_drag["moved"] = True
            self.float_win.geometry(
                f"+{event.x_root - self._float_drag['dx']}"
                f"+{event.y_root - self._float_drag['dy']}")
        except Exception:
            pass

    def _float_release(self, _event):
        moved = bool(self._float_drag and self._float_drag.get("moved"))
        self._float_drag = None
        if not moved:
            self._toggle_float_panel()

    def _toggle_float_panel(self):
        try:
            if (self.float_panel is not None
                    and self.float_panel.winfo_exists()
                    and self.float_panel.winfo_viewable()):
                self.float_panel.withdraw()
                return
            self._show_float_panel()
        except Exception:
            pass

    def _show_float_panel(self):
        try:
            if self.float_panel is None or not self.float_panel.winfo_exists():
                p = tk.Toplevel(self.root)
                p.overrideredirect(True)
                try:
                    p.attributes("-topmost", True)
                except Exception:
                    pass
                p.configure(bg=PANEL)
                tk.Label(p, text="NEXORA", font=("Segoe UI", 11, "bold"),
                         fg="#5b8cff", bg=PANEL).pack(padx=10, pady=(8, 2))
                self._panel_voice_btn = tk.Button(
                    p, text="🎤 Voice: OFF", font=("Segoe UI", 11, "bold"),
                    bg="#2b5cff", fg="white", activebackground="#1e44bd",
                    command=self.toggle_listening)
                self._panel_voice_btn.pack(padx=10, pady=4, fill="x")
                rowp = tk.Frame(p, bg=PANEL)
                rowp.pack(padx=10, pady=4, fill="x")
                tk.Label(rowp, text="⌨", font=("Segoe UI", 12), fg="#9fd0ff",
                         bg=PANEL).pack(side="left")
                self.float_entry = tk.Entry(rowp, font=("Segoe UI", 11), width=16,
                                            bg="#0e1430", fg="#eef1ff",
                                            insertbackground="#eef1ff")
                self.float_entry.pack(side="left", padx=4)
                self.float_entry.bind("<Return>", lambda _e: self._panel_do_it())
                tk.Button(rowp, text="✔", font=("Segoe UI", 11, "bold"),
                          command=self._panel_do_it).pack(side="left")
                tk.Button(p, text="⌂ Home", font=("Segoe UI", 10),
                          bg=CARD, fg="white", activebackground="#28336a",
                          command=self.show_home).pack(padx=10, pady=4, fill="x")
                tk.Button(p, text="✕ Hide icon", font=("Segoe UI", 10),
                          bg=CARD, fg="white", activebackground="#28336a",
                          command=self.hide_floating).pack(padx=10, pady=(4, 8), fill="x")
                self.float_panel = p
            fx = self.float_win.winfo_x()
            fy = self.float_win.winfo_y()
            self.float_panel.deiconify()
            self.float_panel.geometry(f"+{max(0, fx - 190)}+{fy + 82}")
            self.float_panel.lift()
            self._refresh_listen_ui()
        except Exception:
            pass

    def _panel_do_it(self):
        try:
            sentence = self.float_entry.get()
            self.float_entry.delete(0, "end")
        except Exception:
            sentence = ""
        if sentence.strip():
            self.show_home()
            self.handle_command(sentence)

    def show_home(self):
        """Bring the Nexora home (main) window to the front."""
        try:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        except Exception:
            pass

    def hide_floating(self):
        try:
            if self.float_panel is not None:
                self.float_panel.withdraw()
            if self.float_win is not None:
                self.float_win.withdraw()
            self.float_visible = False
            btn = self.circle_btns.get("floating")
            if btn:
                btn["canvas"].itemconfigure(btn["label"], text="Floating: OFF")
        except Exception:
            pass

    def toggle_floating(self):
        """Floating circle button: hide the floating icon, or bring it back."""
        try:
            if self.float_visible:
                self.hide_floating()
            else:
                if self.float_win is None:
                    self._build_floating()
                else:
                    self.float_win.deiconify()
                    try:
                        self.float_win.attributes("-topmost", True)
                    except Exception:
                        pass
                    self.float_win.lift()
                self.float_visible = True
                btn = self.circle_btns.get("floating")
                if btn:
                    btn["canvas"].itemconfigure(btn["label"], text="Floating")
        except Exception:
            pass

    # ----- basics: v6 two-sided logging -----
    @staticmethod
    def _pane_append(text_widget, text):
        text_widget.configure(state="normal")
        text_widget.insert("end", text + "\n")
        text_widget.see("end")
        text_widget.configure(state="disabled")

    def log_user(self, text):
        """What the USER said/typed -> LEFT pane only."""
        try:
            self._pane_append(self.user_text.text_widget, text)
        except Exception:
            pass

    def log_nexora(self, text):
        """What NEXORA did / replied / reports -> RIGHT pane only."""
        try:
            self._pane_append(self.nexora_text.text_widget, text)
        except Exception:
            pass

    def log(self, text):
        """Nexora-side message (startup notes, status, results)."""
        self.log_nexora(text)

    def user_log_text(self):
        try:
            return self.user_text.text_widget.get("1.0", "end")
        except Exception:
            return ""

    def nexora_log_text(self):
        try:
            return self.nexora_text.text_widget.get("1.0", "end")
        except Exception:
            return ""

    def log_text(self):
        """Both panes combined (diagnostics/smoke tests)."""
        return self.user_log_text() + "\n" + self.nexora_log_text()

    def set_status(self, text):
        self.status_var.set(text)

    def speak(self, text):
        if not self.speak_var.get() or pyttsx3 is None:
            return
        lang = self.language_code().split("-")[0].lower()
        def _talk():
            try:
                if self.tts_engine is None:
                    self.tts_engine = pyttsx3.init()
                # Best effort: if Windows has a voice for the selected
                # language, use it; otherwise the default voice reads
                # the (localised) text - never a crash either way.
                try:
                    for voice in self.tts_engine.getProperty("voices"):
                        blob = " ".join([
                            str(getattr(voice, "id", "")),
                            str(getattr(voice, "name", "")),
                            " ".join(str(x) for x in (getattr(voice, "languages", None) or [])),
                        ]).lower()
                        if lang and lang in blob:
                            self.tts_engine.setProperty("voice", voice.id)
                            break
                except Exception:
                    pass
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception:
                pass  # silent fallback - never crash on TTS
        threading.Thread(target=_talk, daemon=True).start()

    def answer(self, message):
        self.log_nexora(message)
        if self.always_listening:
            self.set_status(self.ui()["listening_on"])
        else:
            self.set_status(self.ui()["ready_status"])
        self.speak(message)

    # ----- command handling -----
    def handle_command(self, sentence, continuous=False):
        sentence = (sentence or "").strip()
        if not sentence:
            return
        self.log_user(sentence)   # v6: user's words -> LEFT pane only
        result = parse_any(sentence)
        if continuous and result.get("action") == "unknown":
            # Always-listen mode: unknown phrases are noted quietly in
            # the Nexora pane - NO spoken "did not understand" (that
            # would spam the user with TTS for background talk).
            self.log_nexora(self.ui()["not_understood"])
            self.set_status(self.ui()["listening_on"])
            return
        message = self.runner.run(result)
        if message:  # dictation/close schedule their own final message
            self.answer(message)
        if self.always_listening:
            self.set_status(self.ui()["listening_on"])

    def on_do_it(self):
        sentence = self.entry.get()
        self.entry.delete(0, "end")
        self.handle_command(sentence)

    # ----- dictation & close (scheduled so the user can switch window) -----
    def schedule_dictation_paste(self, text):
        copied = False
        try:
            if pyperclip is not None:
                pyperclip.copy(text)
                copied = True
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                copied = True
        except Exception:
            copied = False
        if not copied:
            self.log("Dictation text (copy it from here): " + text)
            return "The text could not be copied to the clipboard - I put it in the log above, please copy it from there."
        self.log(f"Dictation ready: \"{text}\" - it will paste in 3 seconds. Quickly click on the Word/Notepad window!")
        self.root.after(3000, lambda: self._do_paste(text))
        return ""  # final message comes from _do_paste

    def _do_paste(self, text):
        typing_reply = replies_for(self.language_code())["typing"].format(text=text)
        try:
            if pyautogui is not None:
                pyautogui.hotkey("ctrl", "v")
                self.answer(typing_reply)
            else:
                self.answer(typing_reply + " (The text is on the clipboard - press Ctrl+V in your window.)")
        except Exception:
            self.answer("Paste failed - press Ctrl+V yourself, the text is on the clipboard.")

    def schedule_close_window(self):
        self.log("The window in front will close in 2 seconds...")
        self.root.after(2000, self._do_close)
        return ""

    def _do_close(self):
        try:
            if pyautogui is not None:
                pyautogui.hotkey("alt", "f4")
                self.answer("Window closed.")
            else:
                self.answer("Closing is not possible (pyautogui is missing) - press Alt+F4 yourself.")
        except Exception:
            self.answer("The window could not be closed.")

    # ----- always-listen (v5): tap 🎤 once, Nexora keeps listening -----
    def toggle_listening(self):
        """The 🎤 Voice circle + the floating panel button call this."""
        if self.always_listening:
            self._stop_listening()
        else:
            self._start_listening()

    def _start_listening(self):
        if sr is None:
            self.answer("The voice library (SpeechRecognition) was not found. Start Nexora with run_nexora.bat - the libraries install themselves. For now, type a command on the right and press the tick button.")
            return
        self.always_listening = True
        self._listen_stop.clear()
        self._listen_error_logged = False
        self._refresh_listen_ui()
        r = self.ui()
        self.set_status(r["listening_on"])
        self.log("🎤 " + r["listening_on"] + " Always-listen is ON - no clicking again for every command. Tap the 🎤 Voice circle button again to stop.")
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()

    def _stop_listening(self):
        self.always_listening = False
        self._listen_stop.set()
        self._refresh_listen_ui()
        r = self.ui()
        self.set_status(r["ready_status"])
        self.log("🎤 " + r["listening_off"] + " Tap the 🎤 Voice circle button to start listening again.")

    def _refresh_listen_ui(self):
        """Voice circle ring/label + floating ring/dot mirror the state."""
        on = bool(self.always_listening)
        ring_color = RING_ON if on else RING_OFF
        try:
            btn = self.circle_btns.get("voice")
            if btn:
                cv = btn["canvas"]
                cv.itemconfigure(btn["ring"], outline=ring_color)
                cv.itemconfigure(btn["glow"], outline=ring_color)
                cv.itemconfigure(btn["label"],
                                 text="Voice: ON" if on else "Voice: OFF")
        except Exception:
            pass
        try:
            if self._float_canvas is not None and self._float_ring is not None:
                self._float_canvas.itemconfigure(self._float_ring,
                                                 outline=ring_color)
            if self._float_canvas is not None and self._float_dot is not None:
                self._float_canvas.itemconfigure(
                    self._float_dot, fill=RING_ON if on else "#555f7a")
        except Exception:
            pass
        try:
            if self._panel_voice_btn is not None:
                self._panel_voice_btn.configure(
                    text="🎤 Voice: ON" if on else "🎤 Voice: OFF")
        except Exception:
            pass

    def _listen_problem(self, message):
        """Log a mic/internet problem at most once per failure streak."""
        if not self._listen_error_logged:
            self._listen_error_logged = True
            try:
                self.root.after(0, lambda m=message: self.log("⚠ " + m))
            except Exception:
                pass

    def _listen_loop(self):
        """
        Background always-listen loop. Runs while always_listening is
        True and NEVER switches itself off: timeouts simply listen
        again, unknown speech is ignored quietly, and mic/internet
        errors are logged once per streak while the loop keeps trying.
        All GUI updates are scheduled with root.after().

        v6 mic robustness: the recognizer re-calibrates for the
        room's ambient noise (0.6s) when the loop starts, and again
        after every 15 failed cycles, so a noisy room or a moved mic
        does not silently break recognition.
        """
        recognizer = None
        fail_cycles = 0
        need_calibration = True   # calibrate once at loop start
        mic_error = None          # localised line, fetched lazily

        def problem_line():
            nonlocal mic_error
            if mic_error is None:
                try:
                    mic_error = replies_for(self.language_code())["mic_error"]
                except Exception:
                    mic_error = ("The microphone could not be heard - "
                                 "please check the mic and your internet.")
            return mic_error

        def note_failure():
            nonlocal fail_cycles, need_calibration
            fail_cycles += 1
            if fail_cycles >= 15:
                fail_cycles = 0
                need_calibration = True   # re-calibrate next cycle

        while not self._listen_stop.is_set():
            if recognizer is None:
                try:
                    recognizer = sr.Recognizer()
                except Exception:
                    self._listen_problem(problem_line())
                    note_failure()
                    self._listen_stop.wait(2.0)
                    continue
            try:
                with sr.Microphone() as source:
                    try:
                        if need_calibration:
                            recognizer.adjust_for_ambient_noise(
                                source, duration=0.6)
                            need_calibration = False
                        else:
                            recognizer.adjust_for_ambient_noise(
                                source, duration=0.3)
                    except Exception:
                        pass
                    audio = recognizer.listen(source, timeout=5,
                                              phrase_time_limit=7)
            except Exception as exc:
                if type(exc).__name__ == "WaitTimeoutError":
                    note_failure()
                    continue  # silence - just listen again, no log spam
                self._listen_problem(problem_line())
                note_failure()
                self._listen_stop.wait(1.0)
                continue
            try:
                heard = recognizer.recognize_google(
                    audio, language=self.language_code())
            except Exception as exc:
                name = type(exc).__name__
                if name == "UnknownValueError":
                    note_failure()
                    continue  # heard something unclear - stay quiet
                self._listen_problem(problem_line())
                note_failure()
                self._listen_stop.wait(1.0)
                continue
            self._listen_error_logged = False
            fail_cycles = 0
            if heard and heard.strip():
                try:
                    self.root.after(
                        0, lambda h=heard: self._handle_heard(h))
                except Exception:
                    pass

    def _handle_heard(self, heard):
        """GUI-thread entry for a phrase heard in always-listen mode."""
        if not self.always_listening:
            return
        self.handle_command(heard, continuous=True)

    # ----- shutdown -----
    def on_close(self):
        """Stop the listen loop cleanly, then close the app."""
        try:
            self.always_listening = False
            self._listen_stop.set()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass


def main():
    if tk is None:
        print("Nexora: Tkinter was not found. On Windows, Tkinter comes with Python itself - please reinstall Python and try again.")
        return
    root = tk.Tk()
    NexoraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
