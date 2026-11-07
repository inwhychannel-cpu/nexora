# Nexora — Voice Laptop Program (Test Version v1)

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

**Zuban badalna:** Upar wale menu se **English (en-US)** ya **Urdu (ur-PK)** chunein.
Roman Urdu commands (jaise "word kholo") English mode mein sab se achi chalti hain.

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
- `nexora_commands.py` — command pehchanne wala hissa (parser)
- `test_commands.py` — parser ke tests (`python test_commands.py` se chalte hain)
- `requirements.txt` — zaroori free libraries ki list
- `run_nexora.bat` — Windows par ek double-click se chalane wali file
- `index.html` — GitHub download page ka namuna (abhi publish NAHI hua)
