"""
Tests for Nexora v5:
- new targets: open_desktop, open_this_pc
- generic open: "open <any app name>" extracts the name; the runner
  then looks the app up and honestly reports when it is not found
  (nothing wrong ever opens)
- smart phrasing: polite lead-ins ("nexora please ...", "and ...",
  "can you ...", "zara ...", "mujhe ...") are stripped at the start
- the v4 traps stay traps: no action fires without a real intent
- the app ALWAYS starts in English: DEFAULT_LOCALE == "en-US"

Run:
    python test_v5.py

Every test prints PASS/FAIL. The last line prints the total count.
No third-party libraries needed.
"""

from nexora_commands import parse_command
from nexora_i18n_commands import parse_command_v2

passed = 0
failed = 0


def check(sentence, expected_action, expected_name=None, parser=parse_command):
    global passed, failed
    result = parser(sentence)
    ok = result.get("action") == expected_action
    if ok and expected_name is not None:
        ok = str(result.get("name", "")).lower() == expected_name.lower()
    if ok:
        passed += 1
        print(f"PASS  {sentence!r:48} -> {result}")
    else:
        failed += 1
        print(f"FAIL  {sentence!r:48} -> got {result}, expected "
              f"action={expected_action} name={expected_name}")


def check_true(label, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"PASS  {label}")
    else:
        failed += 1
        print(f"FAIL  {label}  {detail}")


# --- New targets: desktop -------------------------------------------
check("open desktop", "open_desktop")
check("desktop kholo", "open_desktop")
check("desktop", "open_desktop")

# --- New targets: this pc / my computer ------------------------------
check("open my computer", "open_this_pc")
check("open this pc", "open_this_pc")
check("my computer", "open_this_pc")
check("this pc", "open_this_pc")
check("my pc", "open_this_pc")
check("pc kholo", "open_this_pc")
check("computer kholo", "open_this_pc")
check("open computer", "open_this_pc")
check("open pc", "open_this_pc")

# --- Generic open: name extraction -----------------------------------
check("open python", "generic_open", "python")
check("python kholo", "generic_open", "python")
check("open whatsapp", "generic_open", "whatsapp")
check("open whatsapp app", "generic_open", "whatsapp")
check("open my whatsapp", "generic_open", "whatsapp")
check("open spotify on my laptop", "generic_open", "spotify")
check("open visual studio code", "generic_open", "visual studio code")
check("open telegram please", "generic_open", "telegram")

# --- Safety: generic open must NOT resurrect the v4 traps ------------
check("close the door and lock it before you leave", "unknown")
check("the volume of this book is very high", "unknown")
check("word games", "unknown")
check("home page", "unknown")
check("my date of birth is a secret", "unknown")
check("whatsapp is a nice app for chatting with my friends", "unknown")

# --- Smart phrasing: lead-ins stripped at the start only -------------
check("nexora please open youtube", "open_youtube")
check("and open youtube", "open_youtube")
check("can you open chrome", "open_chrome")
check("could you open word", "open_word")
check("hey nexora open notepad", "open_notepad")
check("please open word", "open_word")
check("zara volume tez karo", "volume_up")
check("mujhe youtube kholo", "open_youtube")
check("and search google for cats", "google_search")
check("nexora", "unknown")

# --- Search query cleanup: leading "and"/"the" dropped ---------------
result = parse_command("and youtube search the cartoon")
check_true("query cleanup: 'and youtube search the cartoon' -> cartoon",
           result.get("action") == "youtube_search"
           and result.get("query") == "cartoon",
           f"got {result}")
result = parse_command_v2("search google for the cats")
check_true("query cleanup via v2: 'search google for the cats' -> cats",
           result.get("action") == "google_search"
           and result.get("query") == "cats",
           f"got {result}")

# --- The app always starts in English ---------------------------------
try:
    import nexora
    check_true("DEFAULT_LOCALE is en-US",
               getattr(nexora, "DEFAULT_LOCALE", None) == "en-US",
               f"got {getattr(nexora, 'DEFAULT_LOCALE', None)!r}")
    # Generic-open runner safety on a non-Windows test machine:
    # an app that does not exist must produce the honest not-found
    # reply (and open nothing).
    class _FakeApp:
        def language_code(self):
            return "en-US"
    runner = nexora.ActionRunner(_FakeApp())
    msg = runner.run({"action": "generic_open", "name": "zzznotanapp"})
    # v6: the not-found reply is the LOCALISED not_found string (the
    # old hardcoded Roman Urdu sentence was removed on purpose).
    check_true("generic_open runner: not-found reply, nothing opened",
               isinstance(msg, str) and "zzznotanapp" in msg
               and "was not found on this laptop" in msg,
               f"got {msg!r}")
    check_true("find_app returns None for a missing app",
               nexora.find_app("zzznotanapp") is None)
except Exception as exc:  # pragma: no cover
    check_true(f"nexora module checks (import failed: {exc})", False)

print()
print(f"RESULT: {passed} passed, {failed} failed, {passed + failed} total")

if __name__ == "__main__":
    raise SystemExit(1 if failed else 0)
