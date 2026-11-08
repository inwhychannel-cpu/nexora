"""
Nexora v2 - Multilingual Command Matcher
=========================================
Pure Python (no third-party libraries).

parse_command_v2(text) works in two steps:

1. The v1 parser (nexora_commands.parse_command) runs first, so
   English and Roman Urdu behave EXACTLY as before.
2. If v1 says "unknown", this module tries command keywords in
   other languages: Urdu (script), Hindi, Arabic, Spanish, French,
   German, Turkish, Russian, Bengali and Punjabi. It understands
   the open / search / type (dictation) / close command WORDS in
   those languages, plus the names of the things to open (Word,
   YouTube, Chrome...) as people say them in those languages.

Honest limit (also in README): in languages NOT in the keyword
tables below, voice dictation and speaking a search still work by
choosing that language in Nexora and using it, but the trained
command *words* on this page are the ~10 languages listed here
(plus English / Roman Urdu from v1).
"""

import re

from nexora_commands import parse_command as _parse_v1
from nexora_commands import normalize_text as _normalize_v1

# Extra punctuation used in Arabic / Urdu / Persian writing
_EXTRA_PUNCT = "،؛؟«»…"


def _unify_chars(s):
    """
    Unify Arabic/Urdu letter variants so one spelling matches the
    other: Arabic yeh -> Urdu yeh, Arabic kaf -> Urdu kaf.
    """
    return s.replace("\u064a", "\u06cc").replace("\u0643", "\u06a9")


def _normalize(text):
    """v1 normalisation + Arabic-script punctuation removal."""
    norm = _normalize_v1(text or "")
    for ch in _EXTRA_PUNCT:
        norm = norm.replace(ch, " ")
    norm = _unify_chars(norm)
    return re.sub(r"\s+", " ", norm).strip()


def _contains_phrase(padded, phrase):
    """Word/phrase-safe containment: ' suche ' in ' ich suche katzen '."""
    return (" " + phrase + " ") in padded


def _find_any(padded, phrases):
    """Return the first phrase from the list found in padded text."""
    for phrase in phrases:
        if _contains_phrase(padded, phrase):
            return phrase
    return None


def _find_anchored(norm, phrases):
    """
    Accuracy rule (v4): return a phrase only if it is the MAIN INTENT
    of the sentence - i.e. the sentence STARTS or ENDS with it. A
    close/search word buried inside a longer unrelated sentence must
    never fire an action.
    """
    for phrase in sorted(phrases, key=len, reverse=True):
        if norm == phrase or norm.startswith(phrase + " ") or norm.endswith(" " + phrase):
            return phrase
    return None


def _remove_phrases(text, phrases):
    """Remove every listed phrase (longest first) from text."""
    out = " " + text + " "
    for phrase in sorted(phrases, key=len, reverse=True):
        out = out.replace(" " + phrase + " ", " ")
    return re.sub(r"\s+", " ", out).strip()


# ---------------------------------------------------------------------------
# Keyword tables
# ---------------------------------------------------------------------------
OPEN_VERBS = [
    # Urdu (script)
    "کھولو", "کھولیں", "کھول دو", "کھول", "چلاؤ",
    # Hindi
    "खोलो", "खोलिए", "खोल दो", "खोल", "चालू करो",
    # Arabic
    "افتح", "شغل", "تشغيل",
    # Spanish
    "abre", "abrir", "abra", "inicia",
    # French
    "ouvre", "ouvrez", "ouvrir", "lance", "lancer",
    # German
    "öffne", "öffnen", "öffnet", "starte", "starten",
    # Turkish
    "aç", "açar", "başlat",
    # Russian
    "открой", "открыть", "запусти", "запустить",
    # Bengali
    "খোলো", "খুলুন", "খোল", "চালু করো",
    # Punjabi
    "ਖੋਲ੍ਹੋ", "ਖੋਲ੍ਹ", "ਚਾਲੂ ਕਰੋ",
]

SEARCH_VERBS = [
    # Urdu (script)
    "تلاش کرو", "تلاش کریں", "ڈھونڈو", "سرچ کرو",
    # Hindi
    "खोजो", "खोजिए", "ढूंढो", "सर्च करो", "खोज",
    # Arabic
    "ابحث عن", "ابحث", "بحث",
    # Spanish
    "busca", "buscar", "búscame",
    # French
    "cherche", "cherchez", "rechercher", "recherche",
    # German
    "suche nach", "suche", "suchen",
    # Turkish
    "arat", "ara", "arama yap",
    # Russian
    "найди", "поищи", "искать", "найти",
    # Bengali
    "খোঁজো", "খুঁজুন", "খোঁজ", "সার্চ করো",
    # Punjabi
    "ਖੋਜੋ", "ਲੱਭੋ", "ਸਰਚ ਕਰੋ",
]

TYPE_VERBS = [
    # sentence-start dictation triggers
    "لکھو", "لکھ دو",              # Urdu (script)
    "लिखो", "लिख दो",                # Hindi
    "اكتب",                          # Arabic
    "escribe", "escribir",          # Spanish
    "écris", "écrire", "tape",      # French
    "schreibe", "schreib", "tippe",  # German
    "yazdır", "yaz",                # Turkish
    "напиши", "напечатай", "пиши",  # Russian
    "লেখো", "লিখুন",                # Bengali
    "ਲਿਖੋ", "ਲਿਖ ਦਿਓ",              # Punjabi
]

CLOSE_VERBS = [
    "بند کرو", "بند کردو",          # Urdu (script)
    "बंद करो", "बन्द करो",          # Hindi
    "أغلق", "اغلق",                  # Arabic
    "cierra", "cerrar", "ciérralo",  # Spanish
    "ferme", "fermez", "fermer",    # French
    "schließe", "schliessen", "schließen", "mach zu",  # German
    "kapat",                        # Turkish
    "закрой", "закрыть",            # Russian
    "বন্ধ করো", "বন্ধ করুন",      # Bengali
    "ਬੰਦ ਕਰੋ",                       # Punjabi
]

# Search filler words removed from the query (per language odds and ends)
SEARCH_FILLERS = [
    "عن", "لي", "للمزيد",            # Arabic bits
    "para", "por", "el", "la", "los", "las", "un", "una",  # Spanish
    "pour", "le", "les", "des", "du", "de",                # French
    "nach", "für", "den", "die", "das", "ein", "eine",     # German
    "için", "bir",                                          # Turkish
    "के लिए", "को", "में",                                  # Hindi
    "کے لیے", "کو",                                         # Urdu
    "এর জন্য",                                              # Bengali
    "ਲਈ",                                                   # Punjabi
    "على", "في", "par", "per", "on", "the", "google", "گوگل", "गूगल",
]

# Things Nexora can open: action -> names people use for it, any language.
TARGETS = [
    ("open_youtube", [
        "youtube", "يوتيوب", "یوٹیوب", "यूट्यूब", "ইউটিউব", "ਯੂਟਿਊਬ", "ютуб",
    ]),
    ("open_word", [
        "microsoft word", "ms word", "word",
        "ورڈ", "وورد", "वर्ड", "ওয়ার্ড", "ਵਰਡ", "ворд",
    ]),
    ("open_chrome", [
        "google chrome", "chrome",
        "کروم", "क्रोम", "ক্রোম", "ਕਰੋਮ", "хром",
    ]),
    ("open_google", [
        "google", "گوگل", "جوجل", "गूगल", "গুগল", "ਗੂਗਲ", "гугл",
    ]),
    ("open_notepad", [
        "notepad", "note pad", "bloc de notas", "bloc-notes", "bloc notes",
        "نوٹ پیڈ", "المفكرة", "مفكرة",
        "नोटपैड", "নোটপ্যাড", "ਨੋਟਪੈਡ", "блокнот",
        "not defteri", "editor",
    ]),
    ("open_calculator", [
        "calculator", "calculadora", "calculatrice", "taschenrechner", "rechner",
        "کیلکولیٹر", "کیلکولیٹر", "الآلة الحاسبة", "آلة حاسبة", "حاسبة",
        "कैलकुलेटर", "कैल्कुलेटर", "ক্যালকুলেটর", "ਕੈਲਕੁਲੇਟਰ", "калькулятор",
        "hesap makinesi",
    ]),
    ("open_paint", [
        "paint", "پینٹ", "الرسام", "पेंट", "পেইন্ট", "ਪੇਂਟ", "пэйнт",
    ]),
    ("open_explorer", [
        "file explorer", "explorer", "files", "file", "dosyalar",
        "فائلیں", "فائل", "ملفات", "ملف",
        "फ़ाइलें", "फाइल", "ফাইলসমূহ", "ফাইল", "ਫ਼ਾਈਲਾਂ", "файлы", "файл",
        "archivos", "archivo", "fichiers", "fichier", "dateien", "ordner",
    ]),
    ("open_pictures", [
        "photos", "photo", "pictures", "picture", "fotos", "fotoğraflar",
        "تصویریں", "تصوير", "صور", "صورة",
        "तस्वीरें", "तस्वीर", "फोटो",
        "ছবি", "তসবিৰ", "তসবির",
        "ਤਸਵੀਰਾਂ", "ਫੋਟੋ", "фото", "фотографии",
    ]),
    ("open_videos", [
        "videos", "video", "vídeos",
        "ویڈیوز", "ویڈیو", "فيديوهات", "فيديو",
        "वीडियो", "ভিডিও", "ਵੀਡੀਓ", "видео",
    ]),
    ("open_downloads", [
        "downloads", "download", "descargas", "téléchargements",
        "ڈاؤن لوڈ", "تنزيلات", "تحميلات",
        "डाउनलोड", "ডাউনলোড", "ਡਾਊਨਲੋਡ", "загрузки",
        "indirmeler", "herunterladen",
    ]),
]

# Apply the same Arabic/Urdu letter unification to every keyword
# table, so matching works no matter which spelling was recognised.
OPEN_VERBS = [_unify_chars(v) for v in OPEN_VERBS]
SEARCH_VERBS = [_unify_chars(v) for v in SEARCH_VERBS]
TYPE_VERBS = [_unify_chars(v) for v in TYPE_VERBS]
CLOSE_VERBS = [_unify_chars(v) for v in CLOSE_VERBS]
SEARCH_FILLERS = [_unify_chars(v) for v in SEARCH_FILLERS]
TARGETS = [(act, [_unify_chars(a) for a in aliases]) for act, aliases in TARGETS]

_ALL_TARGET_ALIASES = [alias for _act, aliases in TARGETS for alias in aliases]
_YOUTUBE_ALIASES = dict(TARGETS)["open_youtube"]
_GOOGLE_ALIASES = dict(TARGETS)["open_google"]


def _find_target(padded):
    """Return (action, alias) of the first target named in the text."""
    for action, aliases in TARGETS:
        for alias in aliases:
            if _contains_phrase(padded, alias):
                return action, alias
    return None, None


def _dictation_payload(original):
    """
    If the sentence STARTS with a dictation word (any keyword language),
    return the rest of the ORIGINAL sentence as the text to type.
    """
    if not original:
        return None
    # Unification is a 1:1 character swap, so indices still align
    # with the original sentence when slicing the payload out of it.
    lowered = _unify_chars(original.lower())
    stripped = lowered.lstrip()
    offset = len(lowered) - len(stripped)
    for verb in sorted(TYPE_VERBS, key=len, reverse=True):
        if stripped.startswith(verb):
            rest = original[offset + len(verb):].strip(" .!؟?،,")
            if rest:
                return rest
    return None


def _extract_query(norm, matched_verb, on_youtube):
    """Build the search query: drop verbs, platform names and fillers."""
    text = _remove_phrases(norm, [matched_verb] if matched_verb else [])
    text = _remove_phrases(text, _YOUTUBE_ALIASES + ["يوتيوب"])
    if not on_youtube:
        text = _remove_phrases(text, _GOOGLE_ALIASES)
    text = _remove_phrases(text, SEARCH_FILLERS)
    # v5: drop a leading English glue word ("...and the cartoon")
    words = text.split()
    while words and words[0] in ("and", "the"):
        words.pop(0)
    return " ".join(words).strip()


def parse_multilingual(text):
    """Try the multilingual keyword matcher. Returns an action dict."""
    original = "" if text is None else str(text).strip()
    norm = _normalize(original)
    if not norm:
        return {"action": "unknown", "text": original}
    padded = " " + norm + " "
    words = norm.split()

    # 1. Dictation first ("लिखो ..." / "اكتب ..." / "escribe ...")
    payload = _dictation_payload(original)
    if payload:
        return {"action": "dictate", "text": payload}

    # 2. Close (anchored only - never from a word inside a sentence)
    if _find_anchored(norm, CLOSE_VERBS):
        return {"action": "close_window"}

    # 3. Search (anchored only - verb at the start or end)
    verb = _find_anchored(norm, SEARCH_VERBS)
    if verb:
        on_youtube = _find_any(padded, _YOUTUBE_ALIASES) is not None
        query = _extract_query(norm, verb, on_youtube)
        if on_youtube:
            if query:
                return {"action": "youtube_search", "query": query}
            return {"action": "open_youtube"}
        if query:
            return {"action": "google_search", "query": query}
        return {"action": "open_google"}

    # 4. Open (open verb + target, or the sentence is EXACTLY the
    #    target's name - "word games" must NOT open Word, see v4 rule)
    action, _alias = _find_target(padded)
    if action and (_find_any(padded, OPEN_VERBS) or norm == _alias):
        return {"action": action}

    return {"action": "unknown", "text": original}


def parse_command_v2(text):
    """
    Full v2 parsing: v1 first (English / Roman Urdu unchanged),
    then the multilingual matcher for the other keyword languages.
    """
    result = _parse_v1(text)
    if result.get("action") != "unknown":
        return result
    return parse_multilingual(text)
