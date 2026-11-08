"""
Nexora - Command Parser
=======================
Pure Python (no third-party libraries).

Takes a spoken or typed sentence in English or Roman Urdu mix and
returns an action dictionary, for example:

    parse_command("word kholo")
    -> {"action": "open_word"}

    parse_command("search for cats")
    -> {"action": "google_search", "query": "cats"}

    parse_command("likho mera naam Ahmad hai")
    -> {"action": "dictate", "text": "mera naam Ahmad hai"}

This file only decides WHAT to do. The actual doing (opening Word,
searching Google, typing, ...) lives in nexora.py.

ACCURACY RULE (v4 - the most important rule in this file)
---------------------------------------------------------
A command only fires when the command phrase is the MAIN INTENT of
the sentence, in a predictable position:

* Dictation words ("likho", "type", ...) must be the FIRST word.
* Search words ("search", "dhundo", "find") must be at the START of
  the sentence, directly NEXT TO a platform name ("search youtube",
  "google search", "youtube ... search karo"), or in the trailing
  Roman Urdu form "... search karo". An explicit search ALWAYS wins
  over open / volume / close / time - so "search google for word
  games" is a Google search for "word games", never "open Word".
* Open commands need an open verb ("open", "kholo", ...) at the
  start or end of the sentence, OR the sentence must be EXACTLY the
  name of the thing ("word", "microsoft word", "youtube"). A target
  word inside a longer sentence never opens anything by itself -
  "word games" is NOT "open Word".
* Close / volume / mute / time / date only fire in short, anchored
  command forms (start or end of the sentence). A word like "close",
  "volume", "time" or "date" appearing inside a longer unrelated
  sentence NEVER triggers an action - the sentence is "unknown" and
  Nexora simply says it did not understand. Doing nothing is always
  better than doing the WRONG thing.

SMART PHRASING (v5)
-------------------
Before the rules above run, the sentence is cleaned by
smart_normalize(): polite lead-ins at the START of the sentence -
"nexora", "please", "and", "can you", "could you", "hey", "ok",
"zara", "mujhe" - are stripped repeatedly, so natural speech like
"nexora please open youtube", "and open youtube" or "can you open
chrome" parses exactly like "open youtube". Only the start is
touched; the same words inside a sentence keep their meaning, and
all the anchored accuracy rules above still apply afterwards.

NEW IN v5: "open desktop", "open my computer / this pc" are real
targets, and an OPEN command for an unknown app name returns
{"action": "generic_open", "name": ...} so the runner can look the
app up on the laptop. Generic open ONLY fires on an anchored open
verb - never for close/volume/time traps.
"""

import re

# Words that mean "open" in English / Roman Urdu
OPEN_WORDS = {"open", "kholo", "khol", "kholoo", "start", "chalao", "chalo", "launch"}

# Search verbs (English / Roman Urdu)
SEARCH_WORDS = {"search", "dhundo", "find"}

# Filler words removed when extracting a search query.
# NOTE: words like "word", "time", "date", "volume", "close" are NOT
# fillers - they can be part of the thing being searched for.
FILLER_WORDS = {
    "please", "kindly", "for", "par", "per", "on", "the", "a", "an",
    "karo", "kar", "do", "mujhe", "mujhy", "ye", "yeh", "wo", "woh",
    "google", "youtube",
}

# Sentences that are EXACTLY a target name open that target.
BARE_TARGETS = {
    "word": "open_word",
    "ms word": "open_word",
    "microsoft word": "open_word",
    "chrome": "open_chrome",
    "google chrome": "open_chrome",
    "notepad": "open_notepad",
    "note pad": "open_notepad",
    "calculator": "open_calculator",
    "calc": "open_calculator",
    "paint": "open_paint",
    "explorer": "open_explorer",
    "file explorer": "open_explorer",
    "files": "open_explorer",
    "youtube": "open_youtube",
    "google": "open_google",
    "photo": "open_pictures",
    "photos": "open_pictures",
    "picture": "open_pictures",
    "pictures": "open_pictures",
    "tasveer": "open_pictures",
    "video": "open_videos",
    "videos": "open_videos",
    "download": "open_downloads",
    "downloads": "open_downloads",
    # v5: the laptop itself
    "desktop": "open_desktop",
    "my computer": "open_this_pc",
    "this pc": "open_this_pc",
    "my pc": "open_this_pc",
}

# Leading words that may precede a short command without changing it
_LEADING_FILLERS = ("please", "nexora", "ok", "okay")


def normalize_text(text):
    """Lowercase, remove punctuation, collapse extra spaces."""
    if not text:
        return ""
    text = str(text).lower().strip()
    # Replace punctuation with a space (keeps word boundaries clean)
    text = re.sub(r"[.,!?;:'\"()\[\]{}<>\\/_\-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Polite lead-ins stripped from the START of a sentence (v5 smart
# phrasing). Two-word forms are checked before single words.
_LEADING_PHRASES = ("can you", "could you")
_LEADING_WORD_FILLERS = {
    "nexora", "please", "and", "hey", "ok", "okay", "zara", "mujhe",
}


def smart_normalize(text):
    """
    normalize_text() + repeatedly strip polite lead-in words/phrases
    from the START of the sentence only:
    "nexora please open youtube" -> "open youtube"
    "and search google for cats" -> "search google for cats"
    Words inside the sentence are never touched.
    """
    norm = normalize_text(text)
    while True:
        stripped = False
        for phrase in _LEADING_PHRASES:
            if norm.startswith(phrase + " "):
                norm = norm[len(phrase) + 1:]
                stripped = True
                break
        if stripped:
            continue
        words = norm.split()
        if len(words) > 1 and words[0] in _LEADING_WORD_FILLERS:
            norm = " ".join(words[1:])
            continue
        return norm


def _extract_query(normalized, extra_remove=None):
    """Remove filler / command words and return the remaining query text."""
    remove = set(FILLER_WORDS)
    remove.update({"search", "dhundo", "find", "look"})
    if extra_remove:
        remove.update(extra_remove)
    words = [w for w in normalized.split() if w not in remove]
    # v5: a natural query often starts with "and ..." ("...and the
    # cartoon") - drop leading glue words from the extracted query.
    while words and words[0] in ("and", "the"):
        words.pop(0)
    return " ".join(words).strip()


def _dictate_payload(original):
    """
    If the sentence STARTS with a dictation word, return the text to
    type. Works on the original (case-preserved) sentence.
    """
    if not original:
        return None
    cleaned = original.strip().strip(" .!?")
    match = re.match(
        r"^(likho|likh do|likhna|type|write|dictate|bolo likho)\s+(.+)$",
        cleaned,
        flags=re.IGNORECASE,
    )
    if match:
        return match.group(2).strip()
    return None


def _core(normalized):
    """Strip one leading filler word ('please', 'nexora', ...)."""
    words = normalized.split()
    if words and words[0] in _LEADING_FILLERS and len(words) > 1:
        return " ".join(words[1:])
    return normalized


def _search_intent(words, normalized):
    """
    Decide whether this sentence is an explicit search, and for where.
    Returns ("youtube" | "google" | None). Anchored forms only (see the
    accuracy rule at the top of this file).
    """
    word_set = set(words)
    if not (word_set & SEARCH_WORDS):
        return None

    has_youtube = "youtube" in word_set
    has_google = "google" in word_set

    # Platform + search verb standing next to each other:
    # "search youtube ...", "youtube search ...", "google search ...",
    # "search google ...", or "youtube/google ... search karo".
    adjacent = False
    for i, w in enumerate(words):
        if w in SEARCH_WORDS:
            neighbours = set()
            if i > 0:
                neighbours.add(words[i - 1])
            if i + 1 < len(words):
                neighbours.add(words[i + 1])
            if neighbours & {"youtube", "google"}:
                adjacent = True
    trailing = normalized.endswith("search karo") or normalized.endswith("search kar do")
    if (has_youtube or has_google) and (adjacent or trailing):
        return "youtube" if has_youtube else "google"

    # Search verb at the very start: "search for cats", "search karo X"
    if words[0] in SEARCH_WORDS:
        return "youtube" if has_youtube else "google"

    # Trailing Roman Urdu form: "<query> search karo"
    if trailing:
        return "youtube" if has_youtube else "google"

    return None


def _volume_action(core_words, core):
    """Volume / mute - anchored, short command forms only."""
    if not core_words:
        return None
    first = core_words[0]
    # Mute: "mute", "awaz band karo" (always mute, never close)
    if core in ("mute", "awaz band karo", "awaz band kar do", "khamosh", "khamosh karo"):
        return "mute"
    if first == "mute" and len(core_words) <= 3:
        return "mute"
    # Volume up/down: sentence must START with volume/awaz and stay short
    if first in ("volume", "awaz", "awaaz") and len(core_words) <= 4:
        word_set = set(core_words)
        if word_set & {"up", "tez", "badhao", "zyada", "increase", "high", "loud"}:
            return "volume_up"
        if word_set & {"down", "kam", "halki", "decrease", "low", "slow"}:
            return "volume_down"
    return None


def _is_close_command(core_words, core):
    """Close window - anchored, short command forms only."""
    if not core_words or len(core_words) > 4:
        return False
    if core in ("band karo", "band kar do", "close", "close this", "close window",
                "close it", "close the window", "close this window"):
        return True
    # "close ..." as the whole short sentence, e.g. "close word"
    if core_words[0] == "close" and len(core_words) <= 3:
        return True
    # "... band karo" as the whole short sentence, e.g. "ye band karo"
    if core.endswith("band karo") and "awaz" not in core_words and "volume" not in core_words:
        return True
    return False


def _is_time_query(core_words, core):
    """Time - anchored question forms only."""
    word_set = set(core_words)
    if not (word_set & {"time", "waqt", "baje", "bajay"}):
        return False
    return (
        core_words[0] in ("what", "time", "waqt", "kitne", "current")
        or core.endswith("batao")
        or "waqt kya" in core
        or "kitne baje" in core
        or len(core_words) <= 3
    )


def _is_date_query(core_words, core):
    """Date - anchored question forms only."""
    word_set = set(core_words)
    if not (word_set & {"date", "tarikh", "tareekh"}):
        return False
    return (
        core_words[0] in ("what", "date", "tarikh", "tareekh")
        or core.endswith("batao")
        or core in ("aaj ki tarikh", "aaj ki date", "aj ki tarikh")
    )


def _open_target(words, normalized):
    """
    Return the open action for a sentence, or None.
    Fires only for an anchored open verb or an exact bare target name.
    """
    word_set = set(words)

    # Exact bare target: the sentence is ONLY the name of the thing.
    if normalized in BARE_TARGETS:
        return BARE_TARGETS[normalized]

    # Open verb anchored at the start ("open youtube", "please open word")
    # or at the end ("word kholo", "youtube kholo").
    core_words = _core(normalized).split()
    anchored_verb = (
        (core_words and core_words[0] in OPEN_WORDS)
        or (core_words and core_words[-1] in OPEN_WORDS)
        or (len(core_words) > 1 and core_words[-2] in OPEN_WORDS)
    )
    if not anchored_verb:
        return None

    if "youtube" in word_set:
        return "open_youtube"
    if "chrome" in word_set:
        return "open_chrome"
    if "google" in word_set:
        return "open_google"
    if "word" in word_set:
        return "open_word"
    if "notepad" in word_set or {"note", "pad"} <= word_set:
        return "open_notepad"
    if "calculator" in word_set or "calc" in word_set:
        return "open_calculator"
    if "paint" in word_set:
        return "open_paint"
    if (
        "explorer" in word_set or "files" in word_set or "folder" in word_set
        or "file" in word_set
    ):
        return "open_explorer"
    if word_set & {"photo", "photos", "picture", "pictures", "tasveer", "tasaveer"}:
        return "open_pictures"
    if word_set & {"video", "videos"}:
        return "open_videos"
    if word_set & {"download", "downloads"}:
        return "open_downloads"
    # v5: the laptop itself
    if "desktop" in word_set:
        return "open_desktop"
    if "computer" in word_set or "pc" in word_set:
        return "open_this_pc"
    # v5: generic open - an anchored open verb + an app name Nexora
    # does not have a built-in target for ("open spotify"). Returns a
    # full result dict; the runner looks the app up on the laptop and
    # honestly reports when it is not found (nothing wrong opens).
    name = _generic_open_name(core_words)
    if name:
        return {"action": "generic_open", "name": name}
    return None


# Words dropped when extracting a generic app name from an open command
_GENERIC_FILLERS = {
    "my", "the", "a", "an", "app", "application", "program",
    "on", "laptop", "please",
}


def _generic_open_name(core_words):
    """
    Extract an app name from an anchored open command:
    ["open", "spotify", "app"] -> "spotify",
    ["whatsapp", "kholo"] -> "whatsapp".
    Returns "" when nothing name-like remains.
    """
    words = list(core_words)
    while words and words[0] in OPEN_WORDS:
        words.pop(0)
    while words and words[-1] in OPEN_WORDS:
        words.pop()
    words = [w for w in words if w not in _GENERIC_FILLERS]
    if not words or len(words) > 4:
        return ""
    if not all(w.isalnum() for w in words):
        return ""
    return " ".join(words)


def parse_command(text):
    """Return an action dict for a spoken/typed sentence."""
    original = "" if text is None else str(text).strip()
    normalized = smart_normalize(original)

    if not normalized:
        return {"action": "unknown", "text": original}

    words = normalized.split()

    # ---- 1. Dictation (checked first: "likho search karo" is dictation) ----
    payload = _dictate_payload(original)
    if payload:
        return {"action": "dictate", "text": payload}

    # ---- 2. Greeting (exact / very short forms only) ----
    if normalized in (
        "hello", "hi", "hey", "salam", "assalamualaikum", "assalam o alaikum",
        "hello nexora", "hi nexora", "salam nexora",
    ) or (words[0] in ("hello", "salam") and len(words) <= 3):
        return {"action": "greet"}

    # ---- 3. Explicit search - ALWAYS wins over open/volume/close/time ----
    where = _search_intent(words, normalized)
    if where == "youtube":
        query = _extract_query(normalized)
        if query:
            return {"action": "youtube_search", "query": query}
        return {"action": "open_youtube"}
    if where == "google":
        query = _extract_query(normalized)
        if query:
            return {"action": "google_search", "query": query}
        return {"action": "open_google"}

    # Short-command core (one leading "please"/"nexora" removed)
    core = _core(normalized)
    core_words = core.split()

    # ---- 4. Volume / mute (before Close, so "awaz band karo" = mute) ----
    vol = _volume_action(core_words, core)
    if vol:
        return {"action": vol}

    # ---- 5. Close window (anchored short forms only) ----
    if _is_close_command(core_words, core):
        return {"action": "close_window"}

    # ---- 6. Time / Date (anchored question forms only) ----
    if _is_time_query(core_words, core):
        return {"action": "tell_time"}
    if _is_date_query(core_words, core):
        return {"action": "tell_date"}

    # ---- 7. Open commands (anchored verb or exact bare target) ----
    opened = _open_target(words, normalized)
    if opened:
        if isinstance(opened, dict):  # generic_open carries the name
            return opened
        return {"action": opened}

    # ---- 8. Unknown - do nothing rather than the wrong thing ----
    return {"action": "unknown", "text": original}
