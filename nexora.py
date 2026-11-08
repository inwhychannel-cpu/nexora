"""
Nexora - Voice Laptop Program (Test Version v4)
================================================
A small Windows program you control with your voice.

- Speak (mic button) or type a command, and Nexora does it:
  opens Word / Chrome / Notepad / YouTube, searches Google/YouTube,
  types what you dictate, tells the time, changes volume, and more.
- v2 speaks the WORLD's languages: pick from 60+ recognition
  languages in the dropdown (nexora_languages.py). Nexora listens
  in that language, replies in that same language (localised reply
  phrases for ~21 languages, English replies for the rest), and
  does the work. Command words are trained for English, Roman Urdu
  and ~10 more languages (nexora_i18n_commands.py).
- English and Roman Urdu commands work exactly as in v1.
- v4 adds the Nexora HOME screen (logo + window icon), a
  "🎤 Voice" button and a "⌨ Type:" command row, and a small
  FLOATING Nexora icon that stays on top of every window - drag
  it anywhere, tap it to give a voice or text command.
- The v4 parser is accuracy-first: a command fires only when it
  is the main intent of the sentence (see nexora_commands.py
  and test_accuracy.py).
- Parsers live in nexora_commands.py (v1) and
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

_FALLBACK_REPLIES = {
    "opening": "Opening {target}.",
    "searching": "Searching for {query}.",
    "typing": "Typing: {text}",
    "not_understood": "Sorry, I did not understand that command.",
    "greeting": "Hello! I am Nexora. What can I do for you?",
    "time_intro": "The time is {value}.",
    "date_intro": "Today's date is {value}.",
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

# ---------------------------------------------------------------------------
# Help text - teaches the user how Nexora works (Help button + popup).
# Simple English, with one short Roman Urdu line at the top.
# ---------------------------------------------------------------------------
HELP_TEXT = """Assalam-o-Alaikum! Nexora aap ki awaaz se aap ka laptop chalata hai - neeche asaan steps diye gaye hain.

WHAT IS NEXORA?
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

HOW TO USE NEXORA - 4 EASY STEPS
1. Choose your language from the list at the top.
2. Click the big blue button:  🎤 Speak
3. Say one command, clearly. (Or type it and press "Do It".)
4. Nexora does the work and replies in your language.

EXAMPLE COMMANDS - TRY THESE
•  open Word
•  open YouTube
•  search Google for cats
•  search YouTube for songs
•  type hello, my name is Ahmad
•  what time is it
•  volume up

TIPS
• Speak slowly and clearly, close to the mic.
• One command at a time.
• If Nexora does not hear you, check your internet and
  your mic, then try again.
• You can also type every command - typing always works.

FLOATING NEXORA ICON - NEW IN v4
A small Nexora "N" icon stays on top of every window.
• Drag it anywhere on the screen - it stays where you drop it.
• Tap (click) it to open a mini panel: a 🎤 Voice button, a
  ⌨ text box with a ✔ button, and a ⌂ Home button that brings
  the Nexora home window forward.
• Hide it from the mini panel (✕ Hide icon) and bring it back
  any time with the "Floating Icon" button in the main window.
"""


# ---------------------------------------------------------------------------
# Small launch helpers (all guarded)
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


def _launch(candidates, friendly_name):
    """
    Try to launch a Windows program from a list of candidates.
    Each candidate is either an exe name (PATH lookup) or a full path.
    Returns (ok: bool, message: str).
    """
    if not IS_WINDOWS:
        return False, f"{friendly_name} sirf Windows par khulta hai - ye laptop Windows ka nahi lagta."
    for cand in candidates:
        try:
            if os.path.isabs(cand):
                if os.path.isfile(cand):
                    os.startfile(cand)  # noqa: S606
                    return True, f"{friendly_name} khol diya."
            else:
                found = shutil.which(cand)
                if found:
                    subprocess.Popen([found])
                    return True, f"{friendly_name} khol diya."
        except Exception:
            continue
    return False, f"{friendly_name} is laptop par nahi mila. Shayad wo install nahi hai."


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
            return f"Ek masla aa gaya ({exc}) - dobara koshish karein."

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
                return "Word laptop par nahi mila, is liye Word ka online version Chrome mein khol diya hai."
            except Exception:
                return msg

        if action == "open_chrome":
            ok, msg = _launch(_chrome_candidates(), "Google Chrome")
            if ok:
                return self._opening(action)
            try:
                webbrowser.open("https://www.google.com")
                return "Chrome nahi mila, is liye default browser mein Google khol diya hai."
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
            return self._opening(action) if _open_folder(home) else "File Explorer nahi khul saka."

        if action == "open_pictures":
            path = os.path.join(os.path.expanduser("~"), "Pictures")
            return self._opening(action) if _open_folder(path) else "Photos wala folder nahi khul saka."

        if action == "open_videos":
            path = os.path.join(os.path.expanduser("~"), "Videos")
            return self._opening(action) if _open_folder(path) else "Videos wala folder nahi khul saka."

        if action == "open_downloads":
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            return self._opening(action) if _open_folder(path) else "Downloads wala folder nahi khul saka."

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
                return "Likhne wali cheez samajh nahi aayi - 'likho' ke baad apna jumla bolein."
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
            return "Volume badalna abhi mumkin nahi (pyautogui library missing hai) - keyboard ke volume button use karein."
        try:
            if action == "mute":
                pyautogui.press("volumemute")
                return "Awaz band kar di (mute)."
            key = "volumeup" if action == "volume_up" else "volumedown"
            for _ in range(5):
                pyautogui.press(key)
            return "Volume tez kar diya." if action == "volume_up" else "Volume kam kar diya."
        except Exception:
            return "Volume nahi badal saka."


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class NexoraApp:
    def __init__(self, root):
        self.root = root
        self.runner = ActionRunner(self)
        self.tts_engine = None
        self.listening = False

        root.title("Nexora \u2014 Home (Test v4)")
        root.geometry("700x720")
        root.minsize(540, 520)
        try:
            root.configure(bg="#0b1020")
        except Exception:
            pass

        # --- Nexora branding: logo on the HOME screen + window icon ---
        # Fully guarded: a missing/failing logo never crashes Nexora.
        self._logo_full = None
        self._logo_img = None       # header-size logo
        self._icon_img = None       # window icon image
        self._float_img = None      # floating-icon image
        try:
            if os.path.isfile(LOGO_PNG):
                _full = tk.PhotoImage(file=LOGO_PNG)      # 800x800 source
                self._logo_full = _full
                self._logo_img = _full.subsample(5, 5)    # ~160px header
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

        if self._logo_img is not None:
            tk.Label(root, image=self._logo_img, bg="#0b1020").pack(pady=(12, 0))
        header = tk.Label(root, text="NEXORA", font=("Segoe UI", 26, "bold"),
                          fg="#5b8cff", bg="#0b1020")
        header.pack(pady=(6, 0))
        tk.Label(root, text="Speak once \u2014 Nexora does it",
                 font=("Segoe UI", 13, "bold"), fg="#eef1ff", bg="#0b1020").pack()
        tk.Label(root, text="Boliye - kaam ho jayega  |  Speak - and it gets done",
                 font=("Segoe UI", 11), fg="#c6cdf5", bg="#0b1020").pack(pady=(0, 8))

        self.status_var = tk.StringVar(value="Status: Tayyar hai (Ready)")
        tk.Label(root, textvariable=self.status_var, font=("Segoe UI", 10, "italic"),
                 fg="#c6cdf5", bg="#0b1020").pack()

        # Language + speak-back row (v2: full world-language list)
        opts = tk.Frame(root, bg="#0b1020")
        opts.pack(pady=8)
        tk.Label(opts, text="Language / Zuban:", fg="#eef1ff", bg="#0b1020").grid(row=0, column=0, padx=4)
        if locale_display_names is not None:
            lang_values = locale_display_names()
        else:
            lang_values = [f"{name} ({code})" for name, code in LANGUAGES]
        self.lang_var = tk.StringVar(value=lang_values[0] if lang_values else "English (US) (en-US)")
        lang_box = ttk.Combobox(opts, textvariable=self.lang_var, state="readonly", width=34,
                                values=lang_values)
        lang_box.grid(row=0, column=1, padx=4)
        self.speak_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opts, text="Bol kar jawab de (Speak back)", variable=self.speak_var,
                       bg="#0b1020", fg="#eef1ff", activebackground="#0b1020",
                       activeforeground="#eef1ff", selectcolor="#1a2342").grid(row=0, column=2, padx=8)

        # Mic button
        self.mic_btn = tk.Button(root, text="🎤 Voice \u2014 Speak (Bolna Shuru Karein)",
                                 font=("Segoe UI", 13, "bold"), bg="#2b5cff", fg="white",
                                 activebackground="#1e44bd", command=self.on_listen_clicked)
        self.mic_btn.pack(pady=6, padx=16, fill="x")

        # Help button - teaches the user how Nexora works
        tk.Button(root, text="❓ Help / How to Use", font=("Segoe UI", 11, "bold"),
                  bg="#1a2342", fg="white", activebackground="#28336a",
                  command=self.show_help).pack(pady=(0, 2), padx=16, fill="x")

        # Floating icon show/hide toggle (the icon itself is built below)
        self.float_btn = tk.Button(root, text="🧭 Floating Icon: ON \u2014 tap to hide / show",
                                   font=("Segoe UI", 11), bg="#1a2342", fg="white",
                                   activebackground="#28336a", command=self.toggle_floating)
        self.float_btn.pack(pady=(0, 2), padx=16, fill="x")

        # Typed command row
        row = tk.Frame(root, bg="#0b1020")
        row.pack(pady=6, padx=16, fill="x")
        tk.Label(row, text="⌨ Type:", font=("Segoe UI", 12, "bold"),
                 fg="#9fd0ff", bg="#0b1020").pack(side="left", padx=(0, 6))
        self.entry = tk.Entry(row, font=("Segoe UI", 12), bg="#121935",
                              fg="#eef1ff", insertbackground="#eef1ff")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.on_do_it())
        tk.Button(row, text="✔ Do It", font=("Segoe UI", 11, "bold"),
                  command=self.on_do_it).pack(side="left", padx=(8, 0))

        tk.Label(root, text="Misal:  word kholo  •  youtube kholo  •  cats search karo  •  likho mera naam Ahmad hai  •  time batao",
                 font=("Segoe UI", 9), fg="#8f9ac9", bg="#0b1020").pack(padx=16, anchor="w")

        tk.Label(root, text=f"🌍 {len(LANGUAGES)} languages: pick yours above — Nexora listens and replies in it. "
                            "Replies are spoken in the selected language when a Windows voice for it is installed; "
                            "otherwise the default Windows voice reads them.",
                 font=("Segoe UI", 9), fg="#555", wraplength=620, justify="left").pack(padx=16, anchor="w")

        # Log area
        self.log_box = scrolledtext.ScrolledText(root, font=("Consolas", 10), height=12, state="disabled",
                                                 bg="#0e1430", fg="#eef1ff", insertbackground="#eef1ff")
        self.log_box.pack(pady=8, padx=16, fill="both", expand=True)

        self.log("👋 Welcome to Nexora v4! Ye aap ki Nexora HOME screen hai - Nexora aap ke laptop ko aap ki awaaz se chalata hai: you speak, Nexora does the work.")
        self.log("How to use:  1) Choose your language above.  2) Click 🎤 Speak.  3) Say a command.  4) Nexora does it and replies in your language.")
        self.log("🌐 Voice works online — internet must be ON.")
        self.log("No mic? Type the command below and press 'Do It'. Need help any time? Click the ❓ Help / How to Use button.")
        self.log(f"🌍 {len(LANGUAGES)} zubanon mein sun sakta hai - upar apni zuban chunein. Jawab usi zuban mein milega (21 bari zubanon ke jawab unhi ki zuban mein, baqi ke liye English).")
        if sr is None:
            self.log("Note: 'SpeechRecognition' library nahi mili - awaaz sunna band hai, lekin typed commands chalengi. run_nexora.bat se chalane par libraries khud install ho jati hain.")
        if pyttsx3 is None:
            self.log("Note: 'pyttsx3' library nahi mili - Nexora bol kar jawab nahi dega, jawab sirf screen par ayega.")
        # Floating Nexora icon (v4) - built last, fully guarded
        self._build_floating()
        if self.float_win is not None:
            self.log("🧭 Floating Nexora icon is ON: it stays on top of every window. Drag it anywhere you like - tap it for 🎤 Voice or ⌨ text, wherever you are.")

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
            tk.Button(win, text="Close / Band Karein", font=("Segoe UI", 11, "bold"),
                      command=win.destroy).pack(pady=(0, 12))
        except Exception:
            # If the popup cannot open, teach in the log instead.
            for line in HELP_TEXT.splitlines():
                self.log(line)

    # ----- floating Nexora icon (v4) -----
    def _build_floating(self):
        """
        Small always-on-top Nexora icon that floats above every other
        window. Drag it anywhere with the mouse; a tap (click without
        dragging) opens a mini panel with 🎤 Voice, a ⌨ text box and a
        ⌂ Home button. Everything is guarded - if the floating window
        cannot be created, the main window simply works without it.
        """
        self.float_win = None
        self.float_panel = None
        self.float_visible = False
        self._float_drag = None
        try:
            win = tk.Toplevel(self.root)
            win.overrideredirect(True)
            try:
                win.attributes("-topmost", True)
            except Exception:
                pass
            try:
                win.configure(bg="#0b1020")
            except Exception:
                pass
            if self._float_img is not None:
                body = tk.Label(win, image=self._float_img, bg="#0b1020",
                                bd=0, cursor="hand2")
            else:
                # Fallback: navy square with a bold cyan "N"
                body = tk.Canvas(win, width=64, height=64, bg="#0b1020",
                                 highlightthickness=0, cursor="hand2")
                body.create_rectangle(4, 4, 60, 60, fill="#121935",
                                      outline="#38e1ff", width=2)
                body.create_text(32, 34, text="N", fill="#38e1ff",
                                 font=("Segoe UI", 30, "bold"))
            body.pack()
            # Bind on the body widget only (its bindtags include the
            # Toplevel, so also binding the window would double-fire).
            body.bind("<ButtonPress-1>", self._float_press)
            body.bind("<B1-Motion>", self._float_move)
            body.bind("<ButtonRelease-1>", self._float_release)
            body.bind("<Button-3>", lambda _e: self.hide_floating())
            try:
                x = max(0, self.root.winfo_screenwidth() - 96)
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
                p.configure(bg="#121935")
                tk.Label(p, text="NEXORA", font=("Segoe UI", 11, "bold"),
                         fg="#5b8cff", bg="#121935").pack(padx=10, pady=(8, 2))
                tk.Button(p, text="🎤 Voice — Speak", font=("Segoe UI", 11, "bold"),
                          bg="#2b5cff", fg="white", activebackground="#1e44bd",
                          command=self._panel_voice).pack(padx=10, pady=4, fill="x")
                rowp = tk.Frame(p, bg="#121935")
                rowp.pack(padx=10, pady=4, fill="x")
                tk.Label(rowp, text="⌨", font=("Segoe UI", 12), fg="#9fd0ff",
                         bg="#121935").pack(side="left")
                self.float_entry = tk.Entry(rowp, font=("Segoe UI", 11), width=16,
                                            bg="#0e1430", fg="#eef1ff",
                                            insertbackground="#eef1ff")
                self.float_entry.pack(side="left", padx=4)
                self.float_entry.bind("<Return>", lambda _e: self._panel_do_it())
                tk.Button(rowp, text="✔", font=("Segoe UI", 11, "bold"),
                          command=self._panel_do_it).pack(side="left")
                tk.Button(p, text="⌂ Home", font=("Segoe UI", 10),
                          bg="#1a2342", fg="white", activebackground="#28336a",
                          command=self.show_home).pack(padx=10, pady=4, fill="x")
                tk.Button(p, text="✕ Hide icon", font=("Segoe UI", 10),
                          bg="#1a2342", fg="white", activebackground="#28336a",
                          command=self.hide_floating).pack(padx=10, pady=(4, 8), fill="x")
                self.float_panel = p
            fx = self.float_win.winfo_x()
            fy = self.float_win.winfo_y()
            self.float_panel.deiconify()
            self.float_panel.geometry(f"+{max(0, fx - 190)}+{fy + 70}")
            self.float_panel.lift()
        except Exception:
            pass

    def _panel_voice(self):
        # Bring the home window forward so the reply/log is visible,
        # then start listening exactly like the main 🎤 button.
        self.show_home()
        self.on_listen_clicked()

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
            self.float_btn.configure(text="🧭 Floating Icon: OFF — tap to show")
        except Exception:
            pass

    def toggle_floating(self):
        """Main-window button: hide the floating icon, or bring it back."""
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
                self.float_btn.configure(text="🧭 Floating Icon: ON — tap to hide / show")
        except Exception:
            pass

    # ----- basics -----
    def log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def set_status(self, text):
        self.status_var.set("Status: " + text)

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
        self.log("Nexora: " + message)
        self.set_status("Tayyar hai (Ready)")
        self.speak(message)

    # ----- command handling -----
    def handle_command(self, sentence):
        sentence = (sentence or "").strip()
        if not sentence:
            return
        self.log("Aap ne kaha: " + sentence)
        self.set_status("Kaam kar raha hai... (Working)")
        result = parse_any(sentence)
        message = self.runner.run(result)
        if message:  # dictation/close schedule their own final message
            self.answer(message)

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
            self.log("Dictation text (copy kar lein): " + text)
            return "Text clipboard par nahi ja saka - upar log mein text de diya hai, wahan se copy kar lein."
        self.log(f"Dictation tayyar hai: \"{text}\" - 3 second mein paste hoga. Jaldi se Word/Notepad ki window par click karein!")
        self.root.after(3000, lambda: self._do_paste(text))
        return ""  # final message comes from _do_paste

    def _do_paste(self, text):
        typing_reply = replies_for(self.language_code())["typing"].format(text=text)
        try:
            if pyautogui is not None:
                pyautogui.hotkey("ctrl", "v")
                self.answer(typing_reply)
            else:
                self.answer(typing_reply + " (Text clipboard par hai - apni window mein Ctrl+V dabayein.)")
        except Exception:
            self.answer("Paste nahi ho saka - Ctrl+V khud dabayein, text clipboard par hai.")

    def schedule_close_window(self):
        self.log("2 second mein samne wali window band hogi...")
        self.root.after(2000, self._do_close)
        return ""

    def _do_close(self):
        try:
            if pyautogui is not None:
                pyautogui.hotkey("alt", "f4")
                self.answer("Window band kar di.")
            else:
                self.answer("Band karna mumkin nahi (pyautogui missing hai) - khud Alt+F4 dabayein.")
        except Exception:
            self.answer("Window band nahi ho saki.")

    # ----- listening -----
    def language_code(self):
        display = self.lang_var.get()
        if code_from_display is not None:
            try:
                return code_from_display(display)
            except Exception:
                pass
        # Fallback parsing if nexora_languages was unavailable
        if "(" in display and ")" in display:
            return display[display.rfind("(") + 1:display.rfind(")")].strip()
        return "en-US"

    def on_listen_clicked(self):
        if self.listening:
            return
        if sr is None:
            self.answer("Awaaz sunne wali library (SpeechRecognition) nahi mili. Pehle run_nexora.bat se program chalayein - libraries khud install ho jayengi. Filhal neeche command likh kar test karein.")
            return
        self.listening = True
        self.mic_btn.configure(text="🔴  Sun raha hai... bolein (Listening...)", state="disabled")
        self.set_status("Sun raha hai... (Listening)")
        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        message = None
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            heard = recognizer.recognize_google(audio, language=self.language_code())
            self.root.after(0, lambda h=heard: self._heard(h))
            return
        except Exception as exc:
            name = type(exc).__name__
            if name == "UnknownValueError":
                message = "Awaaz samajh nahi aayi - zara saaf aur qareeb se bolein."
            elif name == "RequestError":
                message = "Voice sunne ke liye internet chahiye - internet check karein."
            elif name in ("WaitTimeoutError",):
                message = "Koi awaaz nahi aayi - mic check karke dobara bolein."
            else:
                message = "Mic se sunna mumkin nahi hua. Mic laga hai aur permission di hai? Typed command se bhi kaam chalega."
        finally:
            self.root.after(0, lambda m=message: self._listen_done(m))

    def _heard(self, heard):
        self.listening = False
        self.mic_btn.configure(text="🎤 Voice \u2014 Speak (Bolna Shuru Karein)", state="normal")
        self.handle_command(heard)

    def _listen_done(self, message):
        self.listening = False
        self.mic_btn.configure(text="🎤 Voice \u2014 Speak (Bolna Shuru Karein)", state="normal")
        if message:
            self.answer(message)
        else:
            self.set_status("Tayyar hai (Ready)")


def main():
    if tk is None:
        print("Nexora: Tkinter nahi mila. Windows par Python ke sath Tkinter khud ata hai - Python dobara install karke dekhein.")
        return
    root = tk.Tk()
    NexoraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
