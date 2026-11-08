# Nexora — Voice Laptop Program (Test Version v6)

**Nexora kya hai?**
Nexora ek chhota sa Windows laptop program hai jo aap ki **awaaz** se chalta hai.
Aap mic mein bolein — "word kholo", "youtube kholo", "ye search karo", "likho..." —
aur Nexora woh kaam kar deta hai. Jawab screen par bhi ata hai aur (agar awaz wala
feature on ho) bol kar bhi milta hai.

*What is Nexora? A small Windows program you control with your voice. Speak a command —
"open Word", "search for this", "type this" — and Nexora does it. English and
Roman Urdu commands both work.*

**Kharcha: Rs 0** — sab free libraries par bana hai.

---

## Windows laptop par chalane ka tareeqa (step-by-step)

1. **Ye folder apne laptop par copy karein** (pura `nexora-voice-assistant` folder).
2. **Python install karein (sirf pehli dafa):**
   - Chrome mein **python.org** kholein → Python download karein (free).
   - Install ke waqt neeche wale box **"Add python.exe to PATH"** par lazmi tick lagayein.
3. **Microsoft Word waghera** jo khulwana hai, woh pehle se laptop par install hona chahiye.
4. **`run_nexora.bat` par double-click karein.**
   - Pehli dafa libraries khud install hongi (internet chahiye, 1–2 minute lag sakte hain).
   - Phir Nexora ki window khul jayegi.
5. **Mic wala button dabayein**, Windows agar mic ki permission mange to **Allow** karein,
   aur saaf awaaz mein command bolein.
6. Mic na ho ya awaaz samajh na aye to koi baat nahi — **neeche box mein command likh kar
   "Do It / Karo"** dabayein, wohi kaam ho jayega.

*English: Copy the folder to your Windows laptop → install Python from python.org
(tick "Add python.exe to PATH") → double-click `run_nexora.bat` → press the mic
button and speak, or type a command and press "Do It".*

**Zuban badalna:** Upar wale menu se apni zuban chunein — v2 mein **62 zubanein**
hain (neeche "Duniya ki zubanein (v2)" wala hissa dekhein).
Roman Urdu commands (jaise "word kholo") English mode mein sab se achi chalti hain.

---

## 🌍 Duniya ki zubanein (v2 — naya)

Nexora v2 ab **duniya ki bari zubanon** mein kaam karta hai:

**Zuban kaise chunein:** Program ke upar wale **Language** menu se apni zuban
chunein — masalan **Urdu (ur-PK)**, **Hindi (hi-IN)**, **Arabic (ar-SA)**,
**Spanish (es-ES)**, **Chinese (zh-CN)** — kul **62 zubanein** hain: English,
Urdu, Hindi, Punjabi, Bengali, Arabic, Persian, Turkish, Spanish, French,
German, Italian, Portuguese, Russian, Ukrainian, Chinese, Japanese, Korean,
Indonesian, Malay, Thai, Vietnamese, Dutch, Polish, Swedish, Tamil, Telugu,
Pashto, Sindhi aur bohat si aur.

**Aap ki zuban mein kya kya hota hai:**
- **Sunna:** Aap jis zuban mein bolein ge, Nexora usi zuban mein sunega aur samjhega.
- **Jawab:** Kaam hone par jawab **usi zuban mein** ata hai — screen par bhi, bol kar bhi.
- **Bol kar likhna (dictation):** Apni zuban mein bolein, wohi alfaaz type ho jayenge.
- **Search:** Apni zuban mein bol kar Google/YouTube par search ho jayega.

**Saaf si limits (honest baat):**
- Jawab wale jumle (masalan "khol raha hoon", "talash kar raha hoon") **21 bari
  zubanon** ke liye unhi ki zuban mein likhe gaye hain: English, Urdu, Hindi,
  Arabic, Spanish, French, German, Turkish, Bengali, Punjabi, Russian, Chinese,
  Japanese, Korean, Portuguese, Italian, Persian, Pashto, Sindhi, Tamil, Telugu.
  **Baqi zubanon ke liye jawab English mein** ata hai — sunna phir bhi aap ki
  zuban mein hi hota hai.
- Command wale **lafz** (kholo / search karo / likho / band karo) in zubanon ke
  liye sikhaye gaye hain: **English, Roman Urdu, Urdu (script), Hindi, Arabic,
  Spanish, French, German, Turkish, Russian, Bengali, Punjabi.** Baqi zubanon
  mein aap bol kar **likh (dictation)** sakte hain aur apni zuban mein bol kar
  search ki baat keh sakte hain; English command lafz bhi har mode mein chalte hain.
- Bol kar jawab bilkul sahi sunai dene ke liye Windows mein us zuban ki
  **voice install** honi chahiye. Voice na ho to jawab phir bhi usi zuban ke
  alfaaz mein ata hai, bas default Windows voice usay parhti hai (lehja
  English jaisa lag sakta hai) — program rukta nahi hai.

---

## Desktop shortcut (optional)

Nexora ka koi installer nahi hai — lekin desktop par us ka apna icon
lagana asaan hai: Nexora wale folder mein `run_nexora.bat` par
**right-click → Send to → Desktop (create shortcut)** karein, phir
desktop wale shortcut par **right-click → Properties → Change Icon… →
Browse…** → usi folder ki **`nexora.ico`** file chunein. Ab desktop par
Nexora ka "N" wala icon hoga; double-click se Nexora khul jayega.

*English: right-click `run_nexora.bat` → Send to → Desktop (create
shortcut), then set the shortcut's icon to `nexora.ico` via
Properties → Change Icon. No installer — just your own shortcut.*

---

## Poori command list (misalon ke sath)

| Kaam | English mein bolein | Roman Urdu mein bolein |
|---|---|---|
| Microsoft Word kholo | "open word" | "word kholo" |
| Chrome kholo | "open chrome" | "chrome kholo" |
| Notepad kholo | "open notepad" | "notepad kholo" |
| Calculator kholo | "open calculator" | "calculator kholo" |
| Paint kholo | "open paint" | "paint kholo" |
| Files / folders kholo | "open explorer" | "file explorer kholo" |
| YouTube kholo | "open youtube" | "youtube kholo" |
| Google kholo | "open google" | "google kholo" |
| Google par search | "search for cats" | "cats search karo" |
| YouTube par search | "youtube search funny videos" | "youtube par songs search karo" |
| Bol kar likhna (dictation) | "type hello world" | "likho mera naam Ahmad hai" |
| Photos wala folder | "open photos" | "photo kholo" |
| Videos wala folder | "open videos" | "video kholo" |
| Downloads wala folder | "open downloads" | "downloads kholo" |
| Waqt poochna | "what is the time" | "time batao" / "waqt kya hai" |
| Tarikh poochna | "what is the date" | "aaj ki tarikh batao" |
| Samne wali window band karna | "close this" | "band karo" |
| Volume tez | "volume up" | "awaz tez karo" |
| Volume kam | "volume down" | "awaz kam karo" |
| Mute | "mute" | "awaz band karo" |
| Salam / hello | "hello" | "salam" |

**Bol kar likhne (dictation) ka tareeqa:** "likho ..." bolne par Nexora text ko
clipboard par rakhta hai aur kehta hai ke 3 second mein paste karega. Us waqt jaldi se
apni Word/Notepad wali window par click kar dein — text wahan likha aa jayega.
Agar auto-paste na ho to khud **Ctrl+V** daba dein, text wahi hoga.

---

## Saaf si limits (honest baat)

- Ye **test version** hai — sirf upar list wale kaam karta hai.
- **Internet lazmi hai** awaaz pehchanne ke liye (voice recognition Google ki free
  service se hota hai). Internet na ho to typed commands phir bhi chalti hain,
  lekin kuch typed commands (search waghera) ke liye bhi internet chahiye hoga.
- **MS Word tabhi khulega jab laptop par Word install ho.** Na ho to Nexora Word ka
  online version Chrome mein khol deta hai.
- Nexora ke paas abhi **AI wala dimagh nahi hai** — ye ChatGPT jaisi baat-cheet ya
  har naye sawal ka jawab nahi de sakta. Sirf sikhaye gaye commands par kaam karta hai.
- **Mic ki permission** aap ko khud deni hogi; bina mic ke sirf typed commands chalengi.
- Awaz Urdu script (ur-PK) mode mein bhi sun sakti hai, lekin Roman Urdu commands
  English mode mein zyada sahi pehchane jate hain.
- Game kholna: Nexora abhi Pictures/Videos/Downloads aur upar wale programs kholta
  hai — kisi khaas installed game ko kholna test version mein nahi hai, woh agle
  version mein har laptop ke hisaab se set hoga.

---

## Files

- `nexora.py` — main program (window, mic, awaz, saare actions)
- `nexora_commands.py` — v1 command parser (English + Roman Urdu)
- `nexora_i18n_commands.py` — v2 parser: v1 ke baad doosri zubanon ke command lafz
  (Urdu script, Hindi, Arabic, Spanish, French, German, Turkish, Russian, Bengali, Punjabi)
- `nexora_languages.py` — 62 zubanon ki list + 21 zubanon ke jawab wale jumle
- `test_commands.py` — v1 parser ke tests (`python test_commands.py`)
- `test_languages.py` — v2 zubanon aur multilingual commands ke tests (`python test_languages.py`)
- `test_accuracy.py` — v4 accuracy tests: command saaf ho tabhi kaam hoga, ghalat kaam kabhi nahi (`python test_accuracy.py`)
- `test_v5.py` — v5 tests: desktop/this-pc, generic open, smart phrasing, English-start (`python test_v5.py`)
- `test_v6.py` — v6 tests: fuzzy repair (destop → desktop), drives, short/go-to commands, play/chalao, GUI string keys (`python test_v6.py`)
- `assets/` — 4 picture tiles + `bg_main.png` (v6: tiles ka dimmed 2x2 background photo); `make_tiles.py` se dobara ban sakti hain
- `USER-GUIDE.md` — users ke liye asaan guide (English + Roman Urdu)
- `nexora.ico`, `nexora-icon.png`, `logo-new.png` — Nexora ka icon / logo (window icon, floating icon aur desktop shortcut ke liye)
- `requirements.txt` — zaroori free libraries ki list
- `run_nexora.bat` — Windows par ek double-click se chalane wali file
- `index.html` — GitHub download page (website wali file, program ka hissa nahi)
