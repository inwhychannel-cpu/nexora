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

NEW IN v6 (from real laptop testing - the recogniser mishears):
* FUZZY TARGET REPAIR: a misheard target word is repaired with
  difflib ("destop" -> desktop, "yotube" -> youtube, "pothon" ->
  python) before the rules run. Only target vocabulary is repaired,
  never verbs, and a protected set of ordinary/parser words ("mera",
  "home", "door", "games", ...) is never rewritten.
* DRIVE LETTERS: "open c drive", "c disk kholo" ->
  {"action": "open_drive", "drive": "C"}.
* GO-TO / POSSESSIVE / BARE forms: "go to X", "take me to X",
  "X mein jao", "my photos folder", bare "documents" / "music".
* PLAY / CHALAO: "play X on youtube", "youtube par X chalao",
  "X chalao" (X not a known target) -> youtube_search for X.
"""

import difflib
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
    # v6: documents and music folders are bare targets too
    "document": "open_documents",
    "documents": "open_documents",
    "music": "open_music",
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


def _target_action(word_set):
    """
    Map a set of (fuzzy-repaired) words to a built-in open action.
    Specific targets win over the generic folder words, so
    "open my photos folder" is Pictures, not File Explorer -
    explorer/files/folder is checked LAST.
    """
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
    if word_set & {"photo", "photos", "picture", "pictures", "fotos", "tasveer", "tasaveer"}:
        return "open_pictures"
    if word_set & {"video", "videos"}:
        return "open_videos"
    if word_set & {"download", "downloads"}:
        return "open_downloads"
    if word_set & {"document", "documents"}:
        return "open_documents"
    if "music" in word_set:
        return "open_music"
    # v5: the laptop itself
    if "desktop" in word_set:
        return "open_desktop"
    if "computer" in word_set or "pc" in word_set:
        return "open_this_pc"
    if word_set & {"explorer", "files", "file", "folder", "folders"}:
        return "open_explorer"
    return None


# Possessive words dropped when a bare phrase is resolved (v6):
# "my photos folder", "mera photos folder" -> "photos".
_POSSESSIVES = {"my", "mera", "meri", "mere"}


def _clean_bare_phrase(normalized):
    """Drop possessives and a trailing 'folder' from a short phrase."""
    words = [w for w in normalized.split() if w not in _POSSESSIVES]
    if words and words[-1] == "folder":
        words.pop()
    return " ".join(words)


def _single_word_target(word):
    """
    A lone known word ("python", "spotify") -> its built-in action,
    or a generic_open dict for app-name vocabulary (python, whatsapp,
    spotify, settings, camera - the runner looks them up).
    """
    if word not in _FUZZY_VOCAB:
        return None
    action = _FUZZY_VOCAB[word]
    if action:
        return action
    return {"action": "generic_open", "name": word}


def _open_target(words, normalized):
    """
    Return the open action for a sentence, or None.
    Fires only for an anchored open verb or an exact bare target name.
    """
    word_set = set(words)

    # Exact bare target: the sentence is ONLY the name of the thing.
    if normalized in BARE_TARGETS:
        return BARE_TARGETS[normalized]

    # v6: possessive / "folder" cleanup - "my photos folder",
    # "mera photos folder", "photos folder" open that folder.
    cleaned = _clean_bare_phrase(normalized)
    probe = cleaned if cleaned else normalized
    if cleaned != normalized and cleaned in BARE_TARGETS:
        return BARE_TARGETS[cleaned]

    # v6: a single known word alone ("python", "destop" - already
    # fuzzy-repaired to "desktop") opens it.
    probe_words = probe.split()
    if len(probe_words) == 1:
        single = _single_word_target(probe_words[0])
        if single:
            return single

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

    action = _target_action(word_set)
    if action:
        return action
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
    "my", "mera", "meri", "mere", "the", "a", "an", "app", "application",
    "program", "on", "laptop", "please",
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


# ---------------------------------------------------------------------------
# v6: fuzzy repair of misheard TARGET words.
#
# The recogniser mishears ("open my destop" for "open my desktop").
# Before the rules run, each word that is NOT already a known word is
# compared against the known-target vocabulary with
# difflib.get_close_matches(word, vocab, n=1, cutoff=0.78) and swapped
# for the canonical spelling. Canonical word -> built-in action, or
# None for app names (python / whatsapp / spotify / settings / camera)
# which go through generic_open so the runner can look them up.
# ---------------------------------------------------------------------------
_FUZZY_VOCAB = {
    "desktop": "open_desktop",
    "downloads": "open_downloads",
    "download": "open_downloads",
    "documents": "open_documents",
    "document": "open_documents",
    "pictures": "open_pictures",
    "picture": "open_pictures",
    "photos": "open_pictures",
    "photo": "open_pictures",
    "fotos": "open_pictures",
    "videos": "open_videos",
    "video": "open_videos",
    "music": "open_music",
    "youtube": "open_youtube",
    "google": "open_google",
    "chrome": "open_chrome",
    "word": "open_word",
    "notepad": "open_notepad",
    "calculator": "open_calculator",
    "calc": "open_calculator",
    "paint": "open_paint",
    "explorer": "open_explorer",
    "python": None,      # app names -> generic_open
    "whatsapp": None,
    "spotify": None,
    "settings": None,
    "camera": None,
}
_FUZZY_WORDS = sorted(_FUZZY_VOCAB)

# Words that must NEVER be fuzzy-rewritten: every keyword/filler the
# parser itself uses (so "mera" can never become "camera" and "home"
# can never become "chrome"), plus ordinary sentence words from the
# accuracy traps and everyday commands.
_NEVER_FUZZY = set()
for _set in (OPEN_WORDS, SEARCH_WORDS, FILLER_WORDS,
             _LEADING_WORD_FILLERS, _LEADING_FILLERS, _GENERIC_FILLERS):
    _NEVER_FUZZY.update(_set)
for _target_name in BARE_TARGETS:
    _NEVER_FUZZY.update(_target_name.split())
_NEVER_FUZZY.update({
    "my", "mera", "meri", "mere",
    "home", "page", "door", "games", "game", "book", "story", "stories",
    "friend", "friends", "movie", "movies", "travel", "lights", "light",
    "house", "window", "windows", "curtains", "zones", "zone", "sounds",
    "sound", "funny", "secret", "birth", "lock", "leave", "folder",
    "folders", "drive", "disk", "play", "jao", "mein", "naam", "note",
    "cricket", "score", "news", "weather", "today", "pakistan",
    "nasheed", "bananas", "banana", "yellow", "fruit", "waqt", "baje",
    "bajay", "tarikh", "tareekh", "batao", "tez", "kam", "halki",
    "band", "awaz", "awaaz", "khamosh", "what", "when", "tell", "date",
    "time", "volume", "mute", "close", "this", "that", "very", "high",
    "cats", "dogs",
})


def _fuzzy_word(word):
    """Repair ONE misheard target word; leave known/other words alone."""
    if word in _FUZZY_VOCAB or word in _NEVER_FUZZY or len(word) < 4:
        return word
    match = difflib.get_close_matches(word, _FUZZY_WORDS, n=1, cutoff=0.78)
    return match[0] if match else word


def _fuzzy_resolve(normalized):
    """Apply _fuzzy_word to every word of the normalised sentence."""
    return " ".join(_fuzzy_word(w) for w in normalized.split())


# ---------------------------------------------------------------------------
# v6: drive letters - "open c drive", "open c disk", "c drive kholo",
# bare "d disk" -> {"action": "open_drive", "drive": "D"}
# ---------------------------------------------------------------------------
_DRIVE_RE = re.compile(
    r"^(?:(?:open|start|launch)\s+)?([a-z])\s+(drive|disk)"
    r"(?:\s+(?:kholo|khol do|open))?$"
)


def _drive_action(core):
    match = _DRIVE_RE.match(core)
    if match:
        return {"action": "open_drive", "drive": match.group(1).upper()}
    return None


# ---------------------------------------------------------------------------
# v6: play / chalao - playing media means YouTube:
# "play X on youtube", "play X", "youtube par X chalao", "X chalao".
# Conservative: a KNOWN target is left to the open rules
# ("youtube chalao" opens YouTube, "word chalao" opens Word).
# ---------------------------------------------------------------------------
_PLAY_FILLERS = {
    "play", "on", "par", "per", "the", "for", "a", "an",
    "youtube", "chalao", "chalo",
}


def _play_intent(words):
    word_set = set(words)
    verb = None
    if "play" in word_set:
        verb = "play"
    elif word_set & {"chalao", "chalo"}:
        verb = "chalao"
    if not verb:
        return None
    rest = [w for w in words
            if w not in _PLAY_FILLERS and w not in _GENERIC_FILLERS]
    while rest and rest[0] in ("and", "the"):
        rest.pop(0)
    if "youtube" in word_set:
        if rest:
            return {"action": "youtube_search", "query": " ".join(rest)}
        if verb == "play":
            return {"action": "open_youtube"}
        return None  # "youtube chalao" -> open rules open YouTube
    if _target_action(word_set):
        return None  # known target -> open rules ("word chalao")
    if rest:
        return {"action": "youtube_search", "query": " ".join(rest)}
    return None


# ---------------------------------------------------------------------------
# v6: go-to forms act as open: "go to X", "take me to X",
# "X mein jao", "X par jao".
# ---------------------------------------------------------------------------
def _goto_action(normalized):
    phrase = None
    if normalized.startswith("go to "):
        phrase = normalized[len("go to "):]
    elif normalized.startswith("take me to "):
        phrase = normalized[len("take me to "):]
    else:
        for suffix in (" mein jao", " par jao", " me jao"):
            if normalized.endswith(suffix):
                phrase = normalized[:-len(suffix)]
                break
    if not phrase:
        return None
    phrase = _clean_bare_phrase(phrase).strip()
    if not phrase:
        return None
    if phrase in BARE_TARGETS:
        return {"action": BARE_TARGETS[phrase]}
    phrase_words = phrase.split()
    action = _target_action(set(phrase_words))
    if action:
        return {"action": action}
    if len(phrase_words) == 1:
        single = _single_word_target(phrase_words[0])
        if single:
            return single if isinstance(single, dict) else {"action": single}
    name = _generic_open_name(phrase_words)
    if name:
        return {"action": "generic_open", "name": name}
    return None


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

    # ---- 2b. Fuzzy repair of misheard target words (v6) ----
    # "open my destop" -> "open my desktop". Only target vocabulary is
    # repaired (never verbs / protected words), and dictation above
    # already used the original sentence, so typed text is untouched.
    resolved = _fuzzy_resolve(normalized)
    if resolved != normalized:
        normalized = resolved
        words = normalized.split()

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

    # ---- 7. Drive letters (v6): "open c drive", "c disk kholo" ----
    drive = _drive_action(core)
    if drive:
        return drive

    # ---- 8. Play / chalao (v6): "play X on youtube", "X chalao" ----
    play = _play_intent(words)
    if play:
        return play

    # ---- 9. Go-to forms (v6): "go to X", "take me to X", "X mein jao" ----
    goto = _goto_action(normalized)
    if goto:
        return goto

    # ---- 10. Open commands (anchored verb or exact bare target) ----
    opened = _open_target(words, normalized)
    if opened:
        if isinstance(opened, dict):  # generic_open carries the name
            return opened
        return {"action": opened}

    # ---- 11. Unknown - do nothing rather than the wrong thing ----
    return {"action": "unknown", "text": original}
