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
"""

import re

# Words that mean "open" in English / Roman Urdu
OPEN_WORDS = {"open", "kholo", "khol", "kholoo", "start", "chalao", "chalo", "launch"}

# Filler words removed when extracting a search query
FILLER_WORDS = {
    "please", "kindly", "for", "par", "per", "on", "the", "a", "an",
    "karo", "kar", "do", "mujhe", "mujhy", "ye", "yeh", "wo", "woh",
    "google", "youtube",
}


def normalize_text(text):
    """Lowercase, remove punctuation, collapse extra spaces."""
    if not text:
        return ""
    text = str(text).lower().strip()
    # Replace punctuation with a space (keeps word boundaries clean)
    text = re.sub(r"[.,!?;:'\"()\[\]{}<>\\/_\-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_query(normalized, extra_remove=None):
    """Remove filler / command words and return the remaining query text."""
    remove = set(FILLER_WORDS)
    remove.update({"search", "dhundo", "find", "look"})
    if extra_remove:
        remove.update(extra_remove)
    words = [w for w in normalized.split() if w not in remove]
    return " ".join(words).strip()


def _has_open_verb(words):
    return any(w in OPEN_WORDS for w in words)


def _dictate_payload(original):
    """
    If the sentence is a dictation command, return the text to type.
    Works on the original (case-preserved) sentence.
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


def parse_command(text):
    """Return an action dict for a spoken/typed sentence."""
    original = "" if text is None else str(text).strip()
    normalized = normalize_text(original)

    if not normalized:
        return {"action": "unknown", "text": original}

    words = normalized.split()
    word_set = set(words)

    # ---- 1. Dictation (checked first: "likho search karo" is dictation) ----
    payload = _dictate_payload(original)
    if payload:
        return {"action": "dictate", "text": payload}

    # ---- 2. Greeting ----
    if normalized in (
        "hello", "hi", "hey", "salam", "assalamualaikum", "assalam o alaikum",
        "hello nexora", "hi nexora", "salam nexora",
    ) or words[0] in ("hello", "salam") and len(words) <= 3:
        return {"action": "greet"}

    # ---- 3. Volume (checked before Close, so "awaz band karo" = mute) ----
    if "mute" in word_set or "khamosh" in normalized or "awaz band" in normalized:
        return {"action": "mute"}
    if (
        ("volume" in word_set or "awaz" in word_set or "awaaz" in word_set)
        and any(w in word_set for w in ("up", "tez", "badhao", "zyada", "increase", "high", "loud"))
    ):
        return {"action": "volume_up"}
    if (
        ("volume" in word_set or "awaz" in word_set or "awaaz" in word_set)
        and any(w in word_set for w in ("down", "kam", "halki", "decrease", "low", "slow"))
    ):
        return {"action": "volume_down"}

    # ---- 4. Close window ----
    if (
        "close" in word_set
        or normalized in ("band karo", "band kar do", "close", "close this")
        or ("band" in word_set and "karo" in word_set and "awaz" not in word_set and "volume" not in word_set)
    ):
        return {"action": "close_window"}

    # ---- 5. Time / Date ----
    if "time" in word_set or "waqt" in word_set or "bajay" in word_set or "baje" in word_set:
        if any(w in word_set for w in ("what", "tell", "batao", "kya", "hai", "the", "current")) or len(words) <= 3:
            return {"action": "tell_time"}
    if (
        "date" in word_set or "tarikh" in word_set or "tareekh" in word_set
        or ("today" in word_set and "date" in normalized)
        or normalized in ("aaj ki tarikh", "aaj ki date", "what is the date", "aj ki tarikh")
    ):
        return {"action": "tell_date"}

    # ---- 6. Searches (before plain "open youtube/google") ----
    is_search = (
        "search" in word_set or "dhundo" in word_set or "find" in word_set
    )
    if is_search:
        if "youtube" in word_set:
            query = _extract_query(normalized)
            if query:
                return {"action": "youtube_search", "query": query}
            return {"action": "open_youtube"}
        query = _extract_query(normalized)
        if query:
            return {"action": "google_search", "query": query}
        return {"action": "open_google"}

    # Roman Urdu trailing form: "<query> search karo"
    if normalized.endswith("search karo") or normalized.endswith("search kar do"):
        query = _extract_query(normalized)
        if query:
            return {"action": "google_search", "query": query}

    # ---- 7. Open commands ----
    has_open = _has_open_verb(words) or len(words) <= 2

    if has_open:
        # YouTube / Google first (they also appear inside search phrases)
        if "youtube" in word_set:
            return {"action": "open_youtube"}
        if word_set & {"chrome"}:
            return {"action": "open_chrome"}
        if "google" in word_set:
            return {"action": "open_google"}
        if "word" in word_set:
            return {"action": "open_word"}
        if "notepad" in word_set or {"note", "pad"} <= word_set:
            return {"action": "open_notepad"}
        if "calculator" in word_set or "calc" in word_set:
            return {"action": "open_calculator"}
        if "paint" in word_set:
            return {"action": "open_paint"}
        if (
            "explorer" in word_set or "files" in word_set or "folder" in word_set
            or "file" in word_set
        ):
            return {"action": "open_explorer"}
        if word_set & {"photo", "photos", "picture", "pictures", "tasveer", "tasaveer"}:
            return {"action": "open_pictures"}
        if word_set & {"video", "videos"}:
            return {"action": "open_videos"}
        if word_set & {"download", "downloads"}:
            return {"action": "open_downloads"}

    # ---- 8. Unknown ----
    return {"action": "unknown", "text": original}
