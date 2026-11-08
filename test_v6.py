"""
Tests for Nexora v6:
- fuzzy repair of misheard TARGET words ("destop" -> desktop) -
  driven by two REAL failures from laptop testing:
    "open my destop" (heard for "open my desktop") and
    "open c disk" (he wanted drive C:)
- drive letters: {"action": "open_drive", "drive": "C"}
- go-to / possessive / bare forms
- play / chalao -> YouTube search
- the v4/v5 traps stay traps (fuzzy must never resurrect them)
- v6 GUI string keys exist for all 21 full reply languages, and the
  English values are pure English (no Roman Urdu words)

Run:
    python test_v6.py
"""

import re

from nexora_commands import parse_command
from nexora_languages import REPLIES, get_replies

passed = 0
failed = 0


def check(sentence, expected_action, expected_field=None, expected_value=None):
    global passed, failed
    result = parse_command(sentence)
    ok = result.get("action") == expected_action
    if ok and expected_field is not None:
        ok = str(result.get(expected_field, "")) == expected_value
    if ok:
        passed += 1
        print(f"PASS  {sentence!r:48} -> {result}")
    else:
        failed += 1
        print(f"FAIL  {sentence!r:48} -> got {result}, expected "
              f"action={expected_action} {expected_field}={expected_value}")


def check_true(label, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"PASS  {label}")
    else:
        failed += 1
        print(f"FAIL  {label}  {detail}")


# --- The two REAL failures from the user's laptop test ---------------
check("open my destop", "open_desktop")          # heard "destop"
check("open c disk", "open_drive", "drive", "C")  # he wanted drive C:

# --- Fuzzy repair of misheard targets --------------------------------
check("open destop", "open_desktop")
check("destop", "open_desktop")
check("open yotube", "open_youtube")
check("search yotube for songs", "youtube_search", "query", "songs")
check("search gogle for cats", "google_search", "query", "cats")
check("open notpad", "open_notepad")
check("open calculater", "open_calculator")
check("open pothon", "generic_open", "name", "python")
check("open fotus", "open_pictures")
check("fotus", "open_pictures")

# --- Drive letters -----------------------------------------------------
check("open c drive", "open_drive", "drive", "C")
check("c drive kholo", "open_drive", "drive", "C")
check("c drive", "open_drive", "drive", "C")
check("open d drive", "open_drive", "drive", "D")
check("d disk", "open_drive", "drive", "D")

# --- Go-to forms act as open -------------------------------------------
check("go to youtube", "open_youtube")
check("go to desktop", "open_desktop")
check("take me to downloads", "open_downloads")
check("photos mein jao", "open_pictures")
check("desktop par jao", "open_desktop")
check("videos mein jao", "open_videos")

# --- Possessive / bare folder forms ------------------------------------
check("my photos folder", "open_pictures")
check("mera photos folder", "open_pictures")
check("photos folder", "open_pictures")
check("open my photos folder", "open_pictures")
check("my videos", "open_videos")
check("documents", "open_documents")
check("music", "open_music")

# --- Play / chalao -> YouTube ------------------------------------------
check("play funny cats on youtube", "youtube_search", "query", "funny cats")
check("play songs", "youtube_search", "query", "songs")
check("youtube par songs chalao", "youtube_search", "query", "songs")
check("songs chalao", "youtube_search", "query", "songs")
check("naat chalao", "youtube_search", "query", "naat")
# ...but a known target with chalao still OPENS it
check("youtube chalao", "open_youtube")
check("word chalao", "open_word")

# --- Safety: fuzzy/go-to/play must not resurrect the traps -------------
check("close the door and lock it before you leave", "unknown")
check("the volume of this book is very high", "unknown")
check("word games", "unknown")
check("home page", "unknown")
check("games", "unknown")
check("play word games", "unknown")
# "open the door": only a generic name lookup ("door") - the runner
# finds nothing and nothing opens; it must NOT become a real target.
_door = parse_command("open the door")
check_true("'open the door' stays generic name 'door' (no real target)",
           _door.get("action") == "generic_open"
           and _door.get("name") == "door",
           f"got {_door}")
_games = parse_command("open games")
check_true("'open games' is a generic name, not a fuzzy target",
           _games.get("action") == "generic_open"
           and _games.get("name") == "games",
           f"got {_games}")
_mera = parse_command("likho mera naam Ahmad hai")
check_true("'mera' is never fuzzy-rewritten (dictation intact)",
           _mera.get("action") == "dictate"
           and _mera.get("text") == "mera naam Ahmad hai",
           f"got {_mera}")

# --- v6 GUI string keys in nexora_languages ----------------------------
NEW_KEYS = ["subtitle", "you_said", "nexora_did", "not_found",
            "not_understood", "listening_on", "listening_off",
            "ready_status", "mic_error", "examples_line",
            "speak_back_label"]
FULL_LANGS = ["en", "ur", "hi", "ar", "es", "fr", "de", "tr", "bn",
              "pa", "ru", "zh", "ja", "ko", "pt", "it", "fa", "ps",
              "sd", "ta", "te"]
for lang in FULL_LANGS:
    rep = REPLIES.get(lang, {})
    missing = [k for k in NEW_KEYS
               if not (isinstance(rep.get(k), str) and rep[k].strip())]
    fmt_ok = True
    try:
        rep["not_found"].format(name="spotify")
    except Exception:
        fmt_ok = False
    check_true(f"strings {lang}: all v6 keys present + not_found formats",
               not missing and fmt_ok, f"missing={missing} fmt_ok={fmt_ok}")

_en_text = " ".join(REPLIES["en"][k] for k in NEW_KEYS)
_MARKERS = ["kaha", "nahi", "kholo", "batao", "karein", "jayega",
            "boliye", "mujhe", "dhundo", "chahiye", "jayegi"]
_found = [m for m in _MARKERS
          if re.search(r"\b" + m + r"\b", _en_text, re.IGNORECASE)]
check_true("en v6 strings contain no Roman Urdu words", not _found,
           f"found {_found}")
check_true("get_replies('ur-PK') carries the v6 keys",
           all(k in get_replies("ur-PK") for k in NEW_KEYS))
check_true("fallback locale (sw-KE) gets the English v6 keys",
           all(k in get_replies("sw-KE") for k in NEW_KEYS))
check_true("ur not_found is Urdu script (no Roman 'nahi mila')",
           "nahi mila" not in REPLIES["ur"]["not_found"])

print()
print(f"RESULT: {passed} passed, {failed} failed, {passed + failed} total")

if __name__ == "__main__":
    raise SystemExit(1 if failed else 0)
