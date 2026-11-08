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


# ---------------------------------------------------------------------------
# v6: GUI text keys, merged into every REPLIES dict below at load time.
#   subtitle         -> tagline line under the logo
#   you_said         -> log label for what the user said
#   nexora_did       -> log label for what Nexora replies/does
#   not_found        -> .format(name="spotify") honest not-found line
#   listening_on/off -> always-listen status lines
#   ready_status     -> idle status line
#   mic_error        -> microphone/internet problem line
#   examples_line    -> example commands shown under the type box
#   speak_back_label -> the speak-back checkbox label
# (not_understood already exists in every dict above.)
# Locales without a written reply set fall back to English, so they
# get the English UI text too - same honest fallback as the replies.
# ---------------------------------------------------------------------------
_UI = {
    "en": {
        "subtitle": "Speak — and it gets done",
        "you_said": "You said:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' was not found on this laptop, so nothing was opened. Please check the name and try again.",
        "listening_on": "Listening is ON — just speak.",
        "listening_off": "Listening is OFF.",
        "ready_status": "Ready",
        "mic_error": "The microphone could not be heard — please check the mic and your internet.",
        "examples_line": "Examples: open Word • open YouTube • search for cats • type my name is Ahmad • tell the time",
        "speak_back_label": "Speak back (voice reply)",
    },
    "ur": {
        "subtitle": "بولیں — کام ہو جائے گا",
        "you_said": "آپ نے کہا:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' اس لیپ ٹاپ پر نہیں ملا — اس لیے کچھ نہیں کھولا۔ نام چیک کر کے دوبارہ کہیں۔",
        "listening_on": "سننا جاری ہے — بس بولیں۔",
        "listening_off": "سننا بند ہے۔",
        "ready_status": "تیار ہے",
        "mic_error": "مائیک سے آواز نہیں آئی — مائیک اور انٹرنیٹ چیک کریں۔",
        "examples_line": "مثالیں: Word کھولیں • YouTube کھولیں • بلیاں تلاش کریں • لکھیں میرا نام احمد ہے • وقت بتائیں",
        "speak_back_label": "بول کر جواب دیں (آواز میں جواب)",
    },
    "hi": {
        "subtitle": "बोलिए — काम हो जाएगा",
        "you_said": "आपने कहा:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' इस लैपटॉप पर नहीं मिला — इसलिए कुछ नहीं खोला गया। नाम जांचकर फिर कहें।",
        "listening_on": "सुनना चालू है — बस बोलिए।",
        "listening_off": "सुनना बंद है।",
        "ready_status": "तैयार है",
        "mic_error": "माइक से आवाज़ नहीं आई — माइक और इंटरनेट जांचें।",
        "examples_line": "उदाहरण: Word खोलें • YouTube खोलें • बिल्लियाँ खोजें • लिखें मेरा नाम अहमद है • समय बताएं",
        "speak_back_label": "बोलकर जवाब दें (आवाज़ में जवाब)",
    },
    "ar": {
        "subtitle": "تحدّث — وسيتم الأمر",
        "you_said": "قلتَ:",
        "nexora_did": "Nexora:",
        "not_found": "لم يتم العثور على '{name}' على هذا الكمبيوتر — لذلك لم يُفتح شيء. تحقق من الاسم وحاول مرة أخرى.",
        "listening_on": "الاستماع يعمل — تحدّث الآن.",
        "listening_off": "الاستماع متوقف.",
        "ready_status": "جاهز",
        "mic_error": "تعذّر السماع عبر الميكروفون — تحقق من الميكروفون والإنترنت.",
        "examples_line": "أمثلة: افتح Word • افتح YouTube • ابحث عن القطط • اكتب اسمي أحمد • أخبرني بالوقت",
        "speak_back_label": "الرد بالصوت",
    },
    "es": {
        "subtitle": "Habla — y se hace",
        "you_said": "Dijiste:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' no se encontró en esta computadora, así que no se abrió nada. Revisa el nombre e inténtalo de nuevo.",
        "listening_on": "Escucha activada — solo habla.",
        "listening_off": "Escucha desactivada.",
        "ready_status": "Listo",
        "mic_error": "No se pudo oír el micrófono — revisa el micrófono y tu internet.",
        "examples_line": "Ejemplos: abre Word • abre YouTube • busca gatos • escribe mi nombre es Ahmad • dime la hora",
        "speak_back_label": "Responder con voz",
    },
    "fr": {
        "subtitle": "Parlez — et c'est fait",
        "you_said": "Vous avez dit :",
        "nexora_did": "Nexora :",
        "not_found": "« {name} » est introuvable sur cet ordinateur — rien n'a été ouvert. Vérifiez le nom et réessayez.",
        "listening_on": "Écoute activée — parlez.",
        "listening_off": "Écoute désactivée.",
        "ready_status": "Prêt",
        "mic_error": "Le microphone n'a pas pu être entendu — vérifiez le micro et votre connexion internet.",
        "examples_line": "Exemples : ouvre Word • ouvre YouTube • cherche des chats • écris mon nom est Ahmad • dis l'heure",
        "speak_back_label": "Répondre à voix haute",
    },
    "de": {
        "subtitle": "Sprich — und es wird erledigt",
        "you_said": "Du hast gesagt:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' wurde auf diesem Laptop nicht gefunden — es wurde nichts geöffnet. Prüfe den Namen und versuch es noch einmal.",
        "listening_on": "Zuhören ist AN — sprich einfach.",
        "listening_off": "Zuhören ist AUS.",
        "ready_status": "Bereit",
        "mic_error": "Das Mikrofon konnte nicht gehört werden — prüfe Mikrofon und Internet.",
        "examples_line": "Beispiele: öffne Word • öffne YouTube • suche nach Katzen • schreibe mein Name ist Ahmad • sag die Uhrzeit",
        "speak_back_label": "Mit Stimme antworten",
    },
    "tr": {
        "subtitle": "Konuş — iş bitsin",
        "you_said": "Dedin ki:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' bu dizüstü bilgisayarda bulunamadı — bu yüzden hiçbir şey açılmadı. Adı kontrol edip tekrar dene.",
        "listening_on": "Dinleme AÇIK — sadece konuş.",
        "listening_off": "Dinleme KAPALI.",
        "ready_status": "Hazır",
        "mic_error": "Mikrofondan ses alınamadı — mikrofonu ve interneti kontrol et.",
        "examples_line": "Örnekler: Word aç • YouTube aç • kedileri ara • yaz benim adım Ahmad • saati söyle",
        "speak_back_label": "Sesli yanıt ver",
    },
    "bn": {
        "subtitle": "বলুন — কাজ হয়ে যাবে",
        "you_said": "আপনি বললেন:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' এই ল্যাপটপে পাওয়া যায়নি — তাই কিছুই খোলা হয়নি। নামটি যাচাই করে আবার বলুন।",
        "listening_on": "শোনা চালু আছে — শুধু বলুন।",
        "listening_off": "শোনা বন্ধ আছে।",
        "ready_status": "প্রস্তুত",
        "mic_error": "মাইক্রোফোনে শোনা যায়নি — মাইক ও ইন্টারনেট যাচাই করুন।",
        "examples_line": "উদাহরণ: Word খুলুন • YouTube খুলুন • বিড়াল খুঁজুন • লিখুন আমার নাম আহমদ • সময় বলুন",
        "speak_back_label": "কণ্ঠে উত্তর দিন",
    },
    "pa": {
        "subtitle": "ਬੋਲੋ — ਕੰਮ ਹੋ ਜਾਵੇਗਾ",
        "you_said": "ਤੁਸੀਂ ਕਿਹਾ:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' ਇਸ ਲੈਪਟਾਪ 'ਤੇ ਨਹੀਂ ਮਿਲਿਆ — ਇਸ ਲਈ ਕੁਝ ਨਹੀਂ ਖੁੱਲ੍ਹਿਆ। ਨਾਮ ਜਾਂਚ ਕੇ ਫਿਰ ਕਹੋ।",
        "listening_on": "ਸੁਣਨਾ ਚਾਲੂ ਹੈ — ਬੱਸ ਬੋਲੋ।",
        "listening_off": "ਸੁਣਨਾ ਬੰਦ ਹੈ।",
        "ready_status": "ਤਿਆਰ ਹੈ",
        "mic_error": "ਮਾਈਕ ਤੋਂ ਸੁਣਾਈ ਨਹੀਂ ਦਿੱਤਾ — ਮਾਈਕ ਅਤੇ ਇੰਟਰਨੈੱਟ ਜਾਂਚੋ।",
        "examples_line": "ਉਦਾਹਰਣ: Word ਖੋਲ੍ਹੋ • YouTube ਖੋਲ੍ਹੋ • ਬਿੱਲੀਆਂ ਖੋਜੋ • ਲਿਖੋ ਮੇਰਾ ਨਾਮ ਅਹਿਮਦ ਹੈ • ਸਮਾਂ ਦੱਸੋ",
        "speak_back_label": "ਬੋਲ ਕੇ ਜਵਾਬ ਦਿਓ",
    },
    "ru": {
        "subtitle": "Скажи — и всё будет сделано",
        "you_said": "Вы сказали:",
        "nexora_did": "Nexora:",
        "not_found": "«{name}» не найден на этом ноутбуке — ничего не было открыто. Проверьте имя и попробуйте ещё раз.",
        "listening_on": "Слушаю — просто говорите.",
        "listening_off": "Прослушивание выключено.",
        "ready_status": "Готово",
        "mic_error": "Не удалось услышать микрофон — проверьте микрофон и интернет.",
        "examples_line": "Примеры: открой Word • открой YouTube • найди кошек • напиши моё имя Ахмад • скажи время",
        "speak_back_label": "Отвечать голосом",
    },
    "zh": {
        "subtitle": "说一句 — 立刻办好",
        "you_said": "你说：",
        "nexora_did": "Nexora：",
        "not_found": "在这台笔记本上没有找到“{name}”，所以没有打开任何东西。请检查名称后重试。",
        "listening_on": "正在聆听 — 请说话。",
        "listening_off": "聆听已关闭。",
        "ready_status": "就绪",
        "mic_error": "听不到麦克风的声音 — 请检查麦克风和网络。",
        "examples_line": "示例：打开 Word • 打开 YouTube • 搜索猫 • 输入我的名字是 Ahmad • 告诉我时间",
        "speak_back_label": "语音回复",
    },
    "ja": {
        "subtitle": "話すだけ — すぐ実行",
        "you_said": "あなた：",
        "nexora_did": "Nexora：",
        "not_found": "「{name}」はこのパソコンに見つかりませんでした — 何も開かれていません。名前を確認してもう一度どうぞ。",
        "listening_on": "聞き取り中 — 話してください。",
        "listening_off": "聞き取りはオフです。",
        "ready_status": "準備完了",
        "mic_error": "マイクの音が聞き取れませんでした — マイクとインターネットを確認してください。",
        "examples_line": "例：Wordを開いて • YouTubeを開いて • 猫を検索 • 入力して 私の名前はAhmad • 時刻を教えて",
        "speak_back_label": "音声で返信する",
    },
    "ko": {
        "subtitle": "말하세요 — 바로 실행됩니다",
        "you_said": "말씀하신 내용:",
        "nexora_did": "Nexora:",
        "not_found": "이 노트북에서 '{name}'을(를) 찾을 수 없어 아무것도 열지 않았습니다. 이름을 확인하고 다시 시도하세요.",
        "listening_on": "듣는 중 — 말씀하세요.",
        "listening_off": "듣기가 꺼져 있습니다.",
        "ready_status": "준비됨",
        "mic_error": "마이크 소리를 들을 수 없습니다 — 마이크와 인터넷을 확인하세요.",
        "examples_line": "예시: Word 열어 • YouTube 열어 • 고양이 검색 • 내 이름 Ahmad 입력 • 시간 알려줘",
        "speak_back_label": "음성으로 답하기",
    },
    "pt": {
        "subtitle": "Fale — e está feito",
        "you_said": "Você disse:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' não foi encontrado neste laptop, por isso nada foi aberto. Verifique o nome e tente de novo.",
        "listening_on": "A escuta está LIGADA — é só falar.",
        "listening_off": "A escuta está DESLIGADA.",
        "ready_status": "Pronto",
        "mic_error": "Não foi possível ouvir o microfone — verifique o microfone e a internet.",
        "examples_line": "Exemplos: abre o Word • abre o YouTube • pesquisa gatos • escreve o meu nome é Ahmad • diz as horas",
        "speak_back_label": "Responder por voz",
    },
    "it": {
        "subtitle": "Parla — ed è fatto",
        "you_said": "Hai detto:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' non è stato trovato su questo laptop, quindi non è stato aperto nulla. Controlla il nome e riprova.",
        "listening_on": "Ascolto ATTIVO — parla pure.",
        "listening_off": "Ascolto DISATTIVATO.",
        "ready_status": "Pronto",
        "mic_error": "Impossibile sentire il microfono — controlla microfono e internet.",
        "examples_line": "Esempi: apri Word • apri YouTube • cerca gatti • scrivi il mio nome è Ahmad • dimmi l'ora",
        "speak_back_label": "Rispondi a voce",
    },
    "fa": {
        "subtitle": "بگویید — انجام می‌شود",
        "you_said": "شما گفتید:",
        "nexora_did": "Nexora:",
        "not_found": "«{name}» در این لپ‌تاپ پیدا نشد — بنابراین چیزی باز نشد. نام را بررسی کنید و دوباره تلاش کنید.",
        "listening_on": "شنیدن فعال است — فقط صحبت کنید.",
        "listening_off": "شنیدن خاموش است.",
        "ready_status": "آماده",
        "mic_error": "صدای میکروفون شنیده نشد — میکروفون و اینترنت را بررسی کنید.",
        "examples_line": "مثال‌ها: Word را باز کن • YouTube را باز کن • گربه‌ها را جستجو کن • بنویس نام من احمد است • ساعت را بگو",
        "speak_back_label": "پاسخ صوتی بده",
    },
    "ps": {
        "subtitle": "ووایه — کار به وشي",
        "you_said": "تا وویل:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' په دې لپټاپ کې ونه موندل شو — نو هیڅ شی پرانیستل شو. نوم وګوره او بیا هڅه وکړه.",
        "listening_on": "اورېدل چالان دي — بس خبرې وکړه.",
        "listening_off": "اورېدل بند دي.",
        "ready_status": "چمتو",
        "mic_error": "د مایک غږ وانه ورېدل شو — مایک او انټرنیټ وګوره.",
        "examples_line": "بېلګې: Word پرانېزه • YouTube پرانېزه • پيشوګانې ولټوه • ولیکه زما نوم احمد دی • وخت ووایه",
        "speak_back_label": "په غږ ځواب ورکړه",
    },
    "sd": {
        "subtitle": "چئو — ڪم ٿي ويندو",
        "you_said": "توهان چيو:",
        "nexora_did": "Nexora:",
        "not_found": "'{name}' هن ليپ ٽاپ تي نه مليو — تنهن ڪري ڪجهه نه کوليو ويو. نالو چيڪ ڪري ٻيهر ڪوشش ڪريو.",
        "listening_on": "ٻڌڻ جاري آهي — بس ڳالهايو.",
        "listening_off": "ٻڌڻ بند آهي.",
        "ready_status": "تيار",
        "mic_error": "مائيڪ مان آواز نه آيو — مائيڪ ۽ انٽرنيٽ چيڪ ڪريو.",
        "examples_line": "مثالون: Word کوليو • YouTube کوليو • ٻليون ڳوليو • لکيو منهنجو نالو احمد آهي • وقت ٻڌايو",
        "speak_back_label": "ڳالهائي جواب ڏيو",
    },
    "ta": {
        "subtitle": "பேசுங்கள் — வேலை முடிந்தது",
        "you_said": "நீங்கள் சொன்னது:",
        "nexora_did": "Nexora:",
        "not_found": "இந்த லேப்டாப்பில் '{name}' கிடைக்கவில்லை — எனவே எதுவும் திறக்கப்படவில்லை. பெயரைச் சரிபார்த்து மீண்டும் முயற்சிக்கவும்.",
        "listening_on": "கேட்பது இயக்கத்தில் உள்ளது — பேசுங்கள்.",
        "listening_off": "கேட்பது நிறுத்தப்பட்டுள்ளது.",
        "ready_status": "தயார்",
        "mic_error": "மைக்கில் கேட்க முடியவில்லை — மைக் மற்றும் இணையத்தைச் சரிபார்க்கவும்.",
        "examples_line": "எடுத்துக்காட்டுகள்: Word திற • YouTube திற • பூனைகளைத் தேடு • தட்டச்சு செய் என் பெயர் Ahmad • நேரத்தைச் சொல்",
        "speak_back_label": "குரலில் பதிலளி",
    },
    "te": {
        "subtitle": "చెప్పండి — పని పూర్తవుతుంది",
        "you_said": "మీరు చెప్పారు:",
        "nexora_did": "Nexora:",
        "not_found": "ఈ ల్యాప్‌టాప్‌లో '{name}' కనబడలేదు — కాబట్టి ఏదీ తెరవలేదు. పేరును తనిఖీ చేసి మళ్లీ ప్రయత్నించండి.",
        "listening_on": "వినడం ఆన్‌లో ఉంది — మాట్లాడండి.",
        "listening_off": "వినడం ఆఫ్‌లో ఉంది.",
        "ready_status": "సిద్ధం",
        "mic_error": "మైక్ వినబడలేదు — మైక్ మరియు ఇంటర్నెట్‌ను తనిఖీ చేయండి.",
        "examples_line": "ఉదాహరణలు: Word తెరువు • YouTube తెరువు • పిల్లులను వెతుకు • టైప్ చేయి నా పేరు Ahmad • సమయం చెప్పు",
        "speak_back_label": "వాయిస్‌తో సమాధానం ఇవ్వండి",
    },
}

for _lang, _ui_strings in _UI.items():
    REPLIES[_lang].update(_ui_strings)


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
