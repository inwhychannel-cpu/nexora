"""
Nexora - Voice Laptop Program (Test Version v1)
================================================
A small Windows program you control with your voice.

- Speak (mic button) or type a command, and Nexora does it:
  opens Word / Chrome / Notepad / YouTube, searches Google/YouTube,
  types what you dictate, tells the time, changes volume, and more.
- English and Roman Urdu commands both work. Command list: README.md
- Parser lives in nexora_commands.py (pure Python).

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

    def run(self, result):
        action = result.get("action", "unknown")
        try:
            return self._run_inner(action, result)
        except Exception as exc:  # absolute safety net
            return f"Ek masla aa gaya ({exc}) - dobara koshish karein."

    def _run_inner(self, action, result):
        if action == "greet":
            return "Salam! Main Nexora hoon. Boliye, kya karun?"

        if action == "open_word":
            ok, msg = _launch(_office_word_candidates(), "Microsoft Word")
            if ok:
                return msg
            # Fallback: Word in the browser
            try:
                webbrowser.open("https://www.office.com/launch/word")
                return "Word laptop par nahi mila, is liye Word ka online version Chrome mein khol diya hai."
            except Exception:
                return msg

        if action == "open_chrome":
            ok, msg = _launch(_chrome_candidates(), "Google Chrome")
            if ok:
                return msg
            try:
                webbrowser.open("https://www.google.com")
                return "Chrome nahi mila, is liye default browser mein Google khol diya hai."
            except Exception:
                return msg

        if action == "open_notepad":
            ok, msg = _launch(["notepad.exe", "notepad"], "Notepad")
            return msg

        if action == "open_calculator":
            ok, msg = _launch(["calc.exe", "calc"], "Calculator")
            return msg

        if action == "open_paint":
            ok, msg = _launch(["mspaint.exe", "mspaint", "pbrush.exe"], "Paint")
            return msg

        if action == "open_explorer":
            home = os.path.expanduser("~")
            return "File Explorer khol diya." if _open_folder(home) else "File Explorer nahi khul saka."

        if action == "open_pictures":
            path = os.path.join(os.path.expanduser("~"), "Pictures")
            return "Photos wala folder khol diya." if _open_folder(path) else "Photos wala folder nahi khul saka."

        if action == "open_videos":
            path = os.path.join(os.path.expanduser("~"), "Videos")
            return "Videos wala folder khol diya." if _open_folder(path) else "Videos wala folder nahi khul saka."

        if action == "open_downloads":
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            return "Downloads wala folder khol diya." if _open_folder(path) else "Downloads wala folder nahi khul saka."

        if action == "open_youtube":
            webbrowser.open("https://www.youtube.com")
            return "YouTube khol diya."

        if action == "open_google":
            webbrowser.open("https://www.google.com")
            return "Google khol diya."

        if action == "google_search":
            query = result.get("query", "").strip()
            if not query:
                webbrowser.open("https://www.google.com")
                return "Google khol diya - search wali cheez samajh nahi aayi."
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))
            return f"Google par search kar diya: {query}"

        if action == "youtube_search":
            query = result.get("query", "").strip()
            if not query:
                webbrowser.open("https://www.youtube.com")
                return "YouTube khol diya - search wali cheez samajh nahi aayi."
            webbrowser.open("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query))
            return f"YouTube par search kar diya: {query}"

        if action == "dictate":
            text = result.get("text", "").strip()
            if not text:
                return "Likhne wali cheez samajh nahi aayi - 'likho' ke baad apna jumla bolein."
            return self.app.schedule_dictation_paste(text)

        if action == "tell_time":
            now = datetime.datetime.now()
            return "Abhi ka waqt hai " + now.strftime("%I:%M %p").lstrip("0") + "."

        if action == "tell_date":
            today = datetime.date.today()
            return "Aaj ki tarikh hai " + today.strftime("%d %B %Y") + "."

        if action == "close_window":
            return self.app.schedule_close_window()

        if action in ("volume_up", "volume_down", "mute"):
            return self._volume(action)

        return "Ye command samajh nahi aayi. Kuch aur bolein - misal: 'word kholo' ya 'youtube kholo'."

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

        root.title("Nexora - Voice Laptop Program (Test v1)")
        root.geometry("640x520")
        root.minsize(520, 420)

        header = tk.Label(root, text="NEXORA", font=("Segoe UI", 26, "bold"), fg="#2b5cff")
        header.pack(pady=(12, 0))
        tk.Label(root, text="Boliye - kaam ho jayega  |  Speak - and it gets done",
                 font=("Segoe UI", 11)).pack(pady=(0, 8))

        self.status_var = tk.StringVar(value="Status: Tayyar hai (Ready)")
        tk.Label(root, textvariable=self.status_var, font=("Segoe UI", 10, "italic")).pack()

        # Language + speak-back row
        opts = tk.Frame(root)
        opts.pack(pady=8)
        tk.Label(opts, text="Language / Zuban:").grid(row=0, column=0, padx=4)
        self.lang_var = tk.StringVar(value="English (en-US)")
        lang_box = ttk.Combobox(opts, textvariable=self.lang_var, state="readonly", width=18,
                                values=["English (en-US)", "Urdu (ur-PK)"])
        lang_box.grid(row=0, column=1, padx=4)
        self.speak_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opts, text="Bol kar jawab de (Speak back)", variable=self.speak_var).grid(row=0, column=2, padx=8)

        # Mic button
        self.mic_btn = tk.Button(root, text="🎤  Mic - Bolna Shuru Karein (Listen)",
                                 font=("Segoe UI", 13, "bold"), bg="#2b5cff", fg="white",
                                 activebackground="#1e44bd", command=self.on_listen_clicked)
        self.mic_btn.pack(pady=6, padx=16, fill="x")

        # Typed command row
        row = tk.Frame(root)
        row.pack(pady=6, padx=16, fill="x")
        self.entry = tk.Entry(row, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.on_do_it())
        tk.Button(row, text="Do It / Karo", font=("Segoe UI", 11, "bold"),
                  command=self.on_do_it).pack(side="left", padx=(8, 0))

        tk.Label(root, text="Misal:  word kholo  •  youtube kholo  •  cats search karo  •  likho mera naam Ahmad hai  •  time batao",
                 font=("Segoe UI", 9), fg="#555").pack(padx=16, anchor="w")

        # Log area
        self.log_box = scrolledtext.ScrolledText(root, font=("Consolas", 10), height=12, state="disabled")
        self.log_box.pack(pady=8, padx=16, fill="both", expand=True)

        self.log("Nexora shuru ho gaya. Mic dabayein aur bolein, ya neeche command likh kar 'Do It' dabayein.")
        if sr is None:
            self.log("Note: 'SpeechRecognition' library nahi mili - awaaz sunna band hai, lekin typed commands chalengi. run_nexora.bat se chalane par libraries khud install ho jati hain.")
        if pyttsx3 is None:
            self.log("Note: 'pyttsx3' library nahi mili - Nexora bol kar jawab nahi dega, jawab sirf screen par ayega.")

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
        def _talk():
            try:
                if self.tts_engine is None:
                    self.tts_engine = pyttsx3.init()
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
        result = parse_command(sentence)
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
        self.speak("Teen second mein likh dunga. Apni window par click karein.")
        self.root.after(3000, lambda: self._do_paste(text))
        return ""  # final message comes from _do_paste

    def _do_paste(self, text):
        try:
            if pyautogui is not None:
                pyautogui.hotkey("ctrl", "v")
                self.answer("Likh diya: " + text)
            else:
                self.answer("Text clipboard par hai - apni window mein Ctrl+V dabayein, text aa jayega.")
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
        return "ur-PK" if "ur-PK" in self.lang_var.get() else "en-US"

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
        self.mic_btn.configure(text="🎤  Mic - Bolna Shuru Karein (Listen)", state="normal")
        self.handle_command(heard)

    def _listen_done(self, message):
        self.listening = False
        self.mic_btn.configure(text="🎤  Mic - Bolna Shuru Karein (Listen)", state="normal")
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
