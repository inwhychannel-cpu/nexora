"""
Nexora v2 - Languages
=====================
Pure Python (no third-party libraries).

Two things live here:

1. LANGUAGES - the list of speech-recognition locales Nexora can
   listen in. The user picks one in the GUI; the recogniser is then
   called with that locale, so a person can speak Urdu, Hindi,
   Arabic, Spanish, Chinese... and be understood in that language.

2. REPLIES - localised spoken replies for the main confirmations
   (opening, searching, typing, not understood, greeting, time/date).
   Replies are written for the ~21 languages below. For every other
   locale in LANGUAGES, Nexora honestly falls back to the English
   replies (see get_replies). Speaking a reply out loud ALSO needs a
   Windows voice for that language; without one, the default Windows
   voice reads the text (see README).
"""

# (display name shown in the dropdown, speech-recognition locale code)
LANGUAGES = [
    ("English (US)", "en-US"),
    ("English (UK)", "en-GB"),
    ("Urdu — اردو (Pakistan)", "ur-PK"),
    ("Hindi — हिन्दी", "hi-IN"),
    ("Punjabi — ਪੰਜਾਬੀ", "pa-IN"),
    ("Bengali — বাংলা", "bn-BD"),
    ("Arabic — العربية (Saudi)", "ar-SA"),
    ("Arabic — العربية (Egypt)", "ar-EG"),
    ("Persian — فارسی", "fa-IR"),
    ("Turkish — Türkçe", "tr-TR"),
    ("Spanish — Español (Spain)", "es-ES"),
    ("Spanish — Español (Mexico)", "es-MX"),
    ("French — Français", "fr-FR"),
    ("German — Deutsch", "de-DE"),
    ("Italian — Italiano", "it-IT"),
    ("Portuguese — Português (Portugal)", "pt-PT"),
    ("Portuguese — Português (Brazil)", "pt-BR"),
    ("Russian — Русский", "ru-RU"),
    ("Ukrainian — Українська", "uk-UA"),
    ("Chinese — 中文 (Simplified)", "zh-CN"),
    ("Chinese — 中文 (Taiwan)", "zh-TW"),
    ("Japanese — 日本語", "ja-JP"),
    ("Korean — 한국어", "ko-KR"),
    ("Indonesian — Bahasa Indonesia", "id-ID"),
    ("Malay — Bahasa Melayu", "ms-MY"),
    ("Thai — ไทย", "th-TH"),
    ("Vietnamese — Tiếng Việt", "vi-VN"),
    ("Dutch — Nederlands", "nl-NL"),
    ("Polish — Polski", "pl-PL"),
    ("Swedish — Svenska", "sv-SE"),
    ("Danish — Dansk", "da-DK"),
    ("Finnish — Suomi", "fi-FI"),
    ("Norwegian — Norsk", "no-NO"),
    ("Greek — Ελληνικά", "el-GR"),
    ("Hebrew — עברית", "he-IL"),
    ("Swahili — Kiswahili", "sw-KE"),
    ("Amharic — አማርኛ", "am-ET"),
    ("Nepali — नेपाली", "ne-NP"),
    ("Sinhala — සිංහල", "si-LK"),
    ("Tamil — தமிழ்", "ta-IN"),
    ("Telugu — తెలుగు", "te-IN"),
    ("Marathi — मराठी", "mr-IN"),
    ("Gujarati — ગુજરાતી", "gu-IN"),
    ("Kannada — ಕನ್ನಡ", "kn-IN"),
    ("Malayalam — മലയാളം", "ml-IN"),
    ("Pashto — پښتو", "ps-AF"),
    ("Sindhi — سنڌي", "sd-PK"),
    ("Serbian — Српски", "sr-RS"),
    ("Croatian — Hrvatski", "hr-HR"),
    ("Czech — Čeština", "cs-CZ"),
    ("Slovak — Slovenčina", "sk-SK"),
    ("Hungarian — Magyar", "hu-HU"),
    ("Romanian — Română", "ro-RO"),
    ("Bulgarian — Български", "bg-BG"),
    ("Catalan — Català", "ca-ES"),
    ("Filipino — Tagalog", "fil-PH"),
    ("Burmese — မြန်မာ", "my-MM"),
    ("Khmer — ខ្មែរ", "km-KH"),
    ("Lao — ລາວ", "lo-LA"),
    ("Uzbek — O'zbek", "uz-UZ"),
    ("Kazakh — Қазақша", "kk-KZ"),
    ("Azerbaijani — Azərbaycan", "az-AZ"),
]

# Reply keys used by nexora.py:
#   opening        -> .format(target="YouTube")
#   searching      -> .format(query="cats")
#   typing         -> .format(text="hello world")
#   not_understood -> plain string
#   greeting       -> plain string
#   time_intro     -> .format(value="4:35 PM")
#   date_intro     -> .format(value="7 November 2026")
REPLIES = {
    "en": {
        "opening": "Opening {target}.",
        "searching": "Searching for {query}.",
        "typing": "Typing: {text}",
        "not_understood": "Sorry, I did not understand that command. Try saying 'open YouTube' or 'search for cats'.",
        "greeting": "Hello! I am Nexora. What can I do for you?",
        "time_intro": "The time is {value}.",
        "date_intro": "Today's date is {value}.",
    },
    "ur": {
        "opening": "{target} کھول رہا ہوں۔",
        "searching": "{query} تلاش کر رہا ہوں۔",
        "typing": "لکھ رہا ہوں: {text}",
        "not_understood": "معذرت، میں یہ حکم نہیں سمجھ سکا۔",
        "greeting": "السلام علیکم! میں Nexora ہوں۔ میں آپ کے لیے کیا کر سکتا ہوں؟",
        "time_intro": "ابھی وقت ہے {value}۔",
        "date_intro": "آج کی تاریخ ہے {value}۔",
    },
    "hi": {
        "opening": "{target} खोल रहा हूँ।",
        "searching": "{query} खोज रहा हूँ।",
        "typing": "लिख रहा हूँ: {text}",
        "not_understood": "माफ़ कीजिए, मैं यह आदेश नहीं समझ पाया।",
        "greeting": "नमस्ते! मैं Nexora हूँ। मैं आपके लिए क्या कर सकता हूँ?",
        "time_intro": "अभी समय है {value}।",
        "date_intro": "आज की तारीख है {value}।",
    },
    "ar": {
        "opening": "جارٍ فتح {target}.",
        "searching": "جارٍ البحث عن {query}.",
        "typing": "أكتب: {text}",
        "not_understood": "عذرًا، لم أفهم هذا الأمر.",
        "greeting": "مرحبًا! أنا Nexora. ماذا يمكنني أن أفعل لك؟",
        "time_intro": "الوقت الآن هو {value}.",
        "date_intro": "تاريخ اليوم هو {value}.",
    },
    "es": {
        "opening": "Abriendo {target}.",
        "searching": "Buscando {query}.",
        "typing": "Escribiendo: {text}",
        "not_understood": "Lo siento, no entendí ese comando.",
        "greeting": "¡Hola! Soy Nexora. ¿Qué puedo hacer por ti?",
        "time_intro": "La hora es {value}.",
        "date_intro": "La fecha de hoy es {value}.",
    },
    "fr": {
        "opening": "Ouverture de {target}.",
        "searching": "Recherche de {query}.",
        "typing": "Je tape : {text}",
        "not_understood": "Désolé, je n'ai pas compris cette commande.",
        "greeting": "Bonjour ! Je suis Nexora. Que puis-je faire pour vous ?",
        "time_intro": "Il est {value}.",
        "date_intro": "Nous sommes le {value}.",
    },
    "de": {
        "opening": "Öffne {target}.",
        "searching": "Suche nach {query}.",
        "typing": "Ich tippe: {text}",
        "not_understood": "Entschuldigung, ich habe diesen Befehl nicht verstanden.",
        "greeting": "Hallo! Ich bin Nexora. Was kann ich für dich tun?",
        "time_intro": "Die Uhrzeit ist {value}.",
        "date_intro": "Heute ist der {value}.",
    },
    "tr": {
        "opening": "{target} açılıyor.",
        "searching": "{query} aranıyor.",
        "typing": "Yazıyorum: {text}",
        "not_understood": "Üzgünüm, bu komutu anlamadım.",
        "greeting": "Merhaba! Ben Nexora. Senin için ne yapabilirim?",
        "time_intro": "Saat şu an {value}.",
        "date_intro": "Bugünün tarihi {value}.",
    },
    "bn": {
        "opening": "{target} খুলছি।",
        "searching": "{query} খুঁজছি।",
        "typing": "লিখছি: {text}",
        "not_understood": "দুঃখিত, আমি এই নির্দেশটি বুঝতে পারিনি।",
        "greeting": "হ্যালো! আমি Nexora। আমি আপনার জন্য কী করতে পারি?",
        "time_intro": "এখন সময় {value}।",
        "date_intro": "আজকের তারিখ {value}।",
    },
    "pa": {
        "opening": "{target} ਖੋਲ੍ਹ ਰਿਹਾ ਹਾਂ।",
        "searching": "{query} ਖੋਜ ਰਿਹਾ ਹਾਂ।",
        "typing": "ਲਿਖ ਰਿਹਾ ਹਾਂ: {text}",
        "not_understood": "ਮਾਫ਼ ਕਰਨਾ, ਮੈਂ ਇਹ ਹੁਕਮ ਨਹੀਂ ਸਮਝਿਆ।",
        "greeting": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ Nexora ਹਾਂ। ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਕੀ ਕਰ ਸਕਦਾ ਹਾਂ?",
        "time_intro": "ਹੁਣ ਸਮਾਂ ਹੈ {value}।",
        "date_intro": "ਅੱਜ ਦੀ ਤਾਰੀਖ ਹੈ {value}।",
    },
    "ru": {
        "opening": "Открываю {target}.",
        "searching": "Ищу {query}.",
        "typing": "Печатаю: {text}",
        "not_understood": "Извините, я не понял эту команду.",
        "greeting": "Здравствуйте! Я Nexora. Что я могу для вас сделать?",
        "time_intro": "Сейчас {value}.",
        "date_intro": "Сегодня {value}.",
    },
    "zh": {
        "opening": "正在打开{target}。",
        "searching": "正在搜索{query}。",
        "typing": "正在输入：{text}",
        "not_understood": "对不起，我没有听懂这个命令。",
        "greeting": "你好！我是 Nexora。我能为您做什么？",
        "time_intro": "现在时间是{value}。",
        "date_intro": "今天的日期是{value}。",
    },
    "ja": {
        "opening": "{target}を開いています。",
        "searching": "{query}を検索しています。",
        "typing": "入力しています：{text}",
        "not_understood": "すみません、その命令が理解できませんでした。",
        "greeting": "こんにちは！私はNexoraです。何をお手伝いしましょうか？",
        "time_intro": "現在の時刻は{value}です。",
        "date_intro": "今日の日付は{value}です。",
    },
    "ko": {
        "opening": "{target}을(를) 열고 있습니다.",
        "searching": "{query}을(를) 검색하고 있습니다.",
        "typing": "입력 중: {text}",
        "not_understood": "죄송합니다. 그 명령을 이해하지 못했습니다.",
        "greeting": "안녕하세요! 저는 Nexora입니다. 무엇을 도와드릴까요?",
        "time_intro": "현재 시간은 {value}입니다.",
        "date_intro": "오늘 날짜는 {value}입니다.",
    },
    "pt": {
        "opening": "Abrindo {target}.",
        "searching": "Pesquisando {query}.",
        "typing": "Digitando: {text}",
        "not_understood": "Desculpe, não entendi esse comando.",
        "greeting": "Olá! Eu sou o Nexora. O que posso fazer por você?",
        "time_intro": "Agora são {value}.",
        "date_intro": "A data de hoje é {value}.",
    },
    "it": {
        "opening": "Apertura di {target} in corso.",
        "searching": "Ricerca di {query} in corso.",
        "typing": "Sto scrivendo: {text}",
        "not_understood": "Scusa, non ho capito quel comando.",
        "greeting": "Ciao! Sono Nexora. Cosa posso fare per te?",
        "time_intro": "Sono le {value}.",
        "date_intro": "La data di oggi è {value}.",
    },
    "fa": {
        "opening": "در حال باز کردن {target}.",
        "searching": "در حال جستجوی {query}.",
        "typing": "در حال نوشتن: {text}",
        "not_understood": "متأسفم، این دستور را متوجه نشدم.",
        "greeting": "سلام! من Nexora هستم. چه کاری می‌توانم برای شما انجام دهم؟",
        "time_intro": "ساعت اکنون {value} است.",
        "date_intro": "تاریخ امروز {value} است.",
    },
    "ps": {
        "opening": "زه {target} پرانیزم.",
        "searching": "د {query} لټون کوم.",
        "typing": "لیکم: {text}",
        "not_understood": "بخښنه غواړم، زه په دې امر پوه نه شوم.",
        "greeting": "سلام! زه Nexora یم. زه ستاسو لپاره څه کولای شم؟",
        "time_intro": "اوس وخت {value} دی.",
        "date_intro": "نن ورځ نېټه {value} ده.",
    },
    "sd": {
        "opening": "{target} کولي رهيو آهيان.",
        "searching": "{query} ڳولي رهيو آهيان.",
        "typing": "لکي رهيو آهيان: {text}",
        "not_understood": "معاف ڪجو، مون کي اهو حڪم سمجهه ۾ نه آيو.",
        "greeting": "سلام! مان Nexora آهيان. مان توهان لاءِ ڇا ڪري سگهان ٿو؟",
        "time_intro": "هن وقت {value} آهي.",
        "date_intro": "اڄ جي تاريخ {value} آهي.",
    },
    "ta": {
        "opening": "{target} ஐத் திறக்கிறேன்.",
        "searching": "{query} ஐத் தேடுகிறேன்.",
        "typing": "தட்டச்சு செய்கிறேன்: {text}",
        "not_understood": "மன்னிக்கவும், அந்தக் கட்டளையை என்னால் புரிந்துகொள்ள முடியவில்லை.",
        "greeting": "வணக்கம்! நான் Nexora. உங்களுக்கு நான் என்ன செய்ய முடியும்?",
        "time_intro": "இப்போது நேரம் {value}.",
        "date_intro": "இன்றைய தேதி {value}.",
    },
    "te": {
        "opening": "{target} తెరుస్తున్నాను.",
        "searching": "{query} కోసం వెతుకుతున్నాను.",
        "typing": "టైప్ చేస్తున్నాను: {text}",
        "not_understood": "క్షమించండి, ఆ ఆదేశం నాకు అర్థం కాలేదు.",
        "greeting": "నమస్కారం! నేను Nexora ని. మీ కోసం నేను ఏమి చేయగలను?",
        "time_intro": "ఇప్పుడు సమయం {value}.",
        "date_intro": "ఈరోజు తేదీ {value}.",
    },
}


def language_of_locale(locale):
    """'ur-PK' -> 'ur', 'zh-CN' -> 'zh', 'en-US' -> 'en'."""
    if not locale:
        return "en"
    return str(locale).replace("_", "-").split("-")[0].lower()


def get_replies(locale):
    """
    Return the REPLIES dict for a locale like 'ur-PK'.
    Languages without a written reply set fall back to English -
    this is deliberate and is stated honestly in the README.
    """
    return REPLIES.get(language_of_locale(locale), REPLIES["en"])


def locale_display_names():
    """Dropdown labels like 'Urdu — اردو (Pakistan) (ur-PK)'."""
    return [f"{name} ({code})" for name, code in LANGUAGES]


def code_from_display(display):
    """'Urdu — اردو (Pakistan) (ur-PK)' -> 'ur-PK' (fallback 'en-US')."""
    text = str(display or "")
    start = text.rfind("(")
    end = text.rfind(")")
    if 0 <= start < end:
        code = text[start + 1:end].strip()
        if "-" in code:
            return code
    return "en-US"
