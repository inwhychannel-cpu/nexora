# Nexora — User Guide

Simple guide. First in **simple English**, then the same in **Roman Urdu**.

---

# Part 1 — Simple English

## What is Nexora?

Nexora is a small program for your Windows laptop.
You control your laptop with your **voice**.

You speak a command, and Nexora does the work:

- Opens programs (Word, Chrome, Notepad, Calculator, Paint…)
- Opens YouTube and Google
- Searches Google and YouTube for you
- Types the words you say (dictation)
- Tells you the time and date
- Changes the volume

Nexora also **speaks back** to you and tells you what it did.
You choose your language — Nexora listens in **62 languages** and
replies in your language (full reply sentences in 21 big languages,
English replies for the rest).

## Online or offline? — Please read this

**Nexora is an ONLINE voice assistant.**

- **Voice needs internet.** When you speak, Nexora uses the
  internet to understand your voice. No internet = voice will
  not work.
- **YouTube and search need internet** (they are websites).
- **Some typed commands can work offline.** If you *type* a
  command for a program that is on your laptop — like
  "open notepad" or "open calculator" — it can work without
  internet.

Simple rule: **keep the internet ON, and everything works.**

## Install — step by step

You do this only one time.

1. **Download** the file `nexora-test-v6.zip`.
2. **Extract (unzip)** it — right-click the file → "Extract All".
   A new folder will appear.
3. **Install Python one time** (free):
   - Open **python.org** in your browser and download Python.
   - Start the install.
   - ⚠️ On the first install screen, tick the box
     **"Add python.exe to PATH"** — this is very important.
   - Finish the install.
4. Go into the Nexora folder and **double-click `run_nexora.bat`**.
   - The first time, Nexora installs its small free libraries
     itself (1–2 minutes, internet needed).
   - Then the Nexora window opens. Done!

## How to use Nexora

1. **Choose your language** from the list at the top of the window.
2. **Click the big blue button: 🎤 Speak.**
   - If Windows asks for microphone permission, click **Allow**.
3. **Say one command**, slowly and clearly.
4. **Nexora does the work** and replies in your language.

No mic? No problem. **Type** the command in the box and press
**Do It** — the same work gets done.

Stuck? Click **❓ Help / How to Use** inside Nexora — it explains
everything again, inside the program.

## Example commands

Say or type these:

| You say | Nexora does |
|---|---|
| "open Word" | Opens Microsoft Word |
| "open YouTube" | Opens YouTube |
| "search Google for cats" | Searches Google for *cats* |
| "search YouTube for songs" | Searches YouTube for *songs* |
| "type hello, my name is Ahmad" | Types your words where you click |
| "what time is it" | Tells you the time |
| "volume up" | Makes the sound louder |

**About "type":** after you say "type …", Nexora waits 3 seconds.
Quickly click inside Word or Notepad — your words will appear there.

## What's new in v4 — the floating Nexora icon

A small Nexora "N" icon now **floats on top of every window** on
your laptop — over Word, over Chrome, over anything.

- **Drag it** with the mouse to any place on the screen. It stays
  where you drop it.
- **Tap it** (click, without dragging) to open a mini panel:
  a 🎤 **Voice** button, a ⌨ **text box** with a ✔ button, and a
  **⌂ Home** button that brings the Nexora home window forward.
- **Hide it** with "✕ Hide icon" in the mini panel, and bring it
  back any time with the **Floating Icon** button in the main
  Nexora window.

Nexora v4 is also stricter about commands: it only acts when your
command is clear. If a sentence is not a clear command, Nexora
says it did not understand instead of doing the wrong thing.

## What's new in v5 — new design + always-listen

The Nexora home window has a **new design**:

- At the top: the Nexora logo and **4 picture tiles** that show
  what Nexora does.
- On the **left**: 4 round (circle) buttons — 🎤 **Voice**,
  🌐 **Language**, ❓ **Help**, 🧭 **Floating**.
- On the **right**: the ⌨ **Type** box and the conversation log.

**Always-listen — no more clicking again and again:**

- Tap the 🎤 **Voice** circle button **one time**. Its ring turns
  **green** and Nexora keeps listening.
- Now just speak your commands one after another — Nexora does
  each one. You do **not** click for every command.
- Tap the same button again to **stop**. Nexora never stops
  listening by itself — it stays ON until you tap it OFF.
- The floating icon mirrors this: its ring is green while
  Nexora is listening, and its panel has the same Voice ON/OFF
  button.

**Language always starts in English.** Nexora does not guess
your language from your country. To change it, tap the 🌐
**Language** circle button and pick your language from the list.
The change lasts only while Nexora is open.

**More things open now — including offline apps:**

- Say **"open desktop"** for your Desktop, **"open my computer"**
  (or "open this pc") for This PC.
- Say **"open" + any app's name** — "open Spotify", "open
  WhatsApp", "open Python". Nexora searches your laptop (Start
  Menu, Desktop, installed programs) and opens it. If the app is
  really not on your laptop, Nexora honestly says so and opens
  nothing.
- You can speak naturally: **"Nexora, please open YouTube"** and
  **"can you open Chrome"** work too.

## What's new in v6 — short commands, drives, two boxes

- **Short commands are enough.** You do not need a full
  sentence: just say **"desktop"**, **"documents"** or
  **"music"** and Nexora opens it.
- **Misheard words are repaired.** If the mic hears
  **"destop"**, Nexora understands **"desktop"**.
- **Drives open too:** say **"open C drive"** (any letter).
- **Two boxes, side by side:** the LEFT box shows what
  **you said**, the RIGHT box shows what **Nexora did** —
  nothing is mixed together any more.
- **The 4 pictures are now the background** of the window,
  dimmed, with the solid writing panels on top — and the
  whole window now fits smaller laptop screens (1366×768)
  with nothing cut off.
- **The screen speaks your language fully:** pick a language
  and every label and message changes to it. With English
  picked, the screen is pure English.

## Desktop shortcut with the Nexora icon (optional)

Want the Nexora icon on your desktop? In the Nexora folder,
**right-click `run_nexora.bat` → Send to → Desktop (create
shortcut)**. Then right-click the new desktop shortcut →
**Properties → Change Icon…** → **Browse…** → pick **`nexora.ico`**
from the Nexora folder → OK. The shortcut will now show the
Nexora "N" — double-click it to start Nexora, just like the .bat
file itself. (Nexora has no installer; this shortcut is simply
your own quick way in.)

## Small troubleshooting

**Nexora cannot hear me / does not understand my voice**

- Check your **internet** — voice works only online.
- Check your **mic** — is it plugged in / turned on?
- Check **mic permission** — Windows Settings → Privacy →
  Microphone → allow apps to use the microphone.
- Speak slowly, clearly, and close to the mic.
- Still stuck? Type the command and press **Do It**.

**"Python is not found" / `run_nexora.bat` does not start**

- Python is not installed, or the PATH box was not ticked.
- Install Python again from **python.org** and this time tick
  **"Add python.exe to PATH"** on the first screen.
- Then double-click `run_nexora.bat` again.

**A program does not open (for example Word)**

- That program must be installed on your laptop first.
- If Word is not installed, Nexora opens Word online in the
  browser instead.

---

# Part 2 — Roman Urdu mein wohi guide

## Nexora kya hai?

Nexora aap ke Windows laptop ke liye ek chhota sa program hai.
Aap apne laptop ko apni **awaaz** se chalate hain.

Aap command bolein, aur Nexora woh kaam kar deta hai:

- Programs kholta hai (Word, Chrome, Notepad, Calculator, Paint…)
- YouTube aur Google kholta hai
- Google aur YouTube par aap ke liye search karta hai
- Jo aap bolein, woh type kar deta hai (bol kar likhna)
- Time aur date bata deta hai
- Volume (awaaz) tez ya kam kar deta hai

Nexora aap ko **bol kar jawab bhi deta hai** aur bata deta hai ke
us ne kya kiya. Aap apni zuban chunein — Nexora **62 zubanon** mein
sunta hai aur aap ki zuban mein jawab deta hai (21 bari zubanon mein
jawab unhi ki zuban mein, baqi ke liye English mein).

## Online hoga ya offline? — Ye lazmi parhein

**Nexora ek ONLINE voice assistant hai.**

- **Awaaz ke liye internet lazmi hai.** Jab aap bolte hain to
  Nexora aap ki awaaz ko internet ke zariye samajhta hai.
  Internet na ho to awaaz kaam nahi karegi.
- **YouTube aur search ke liye bhi internet chahiye** (ye websites hain).
- **Kuch typed commands offline bhi chal sakti hain.** Agar aap
  command *likh* kar dein kisi aisay program ke liye jo aap ke
  laptop par pehle se hai — jaise "open notepad" ya
  "open calculator" — to woh baghair internet ke bhi chal sakti hai.

Asaan usool: **internet ON rakhein, sab kuch chalega.**

## Install — step by step

Ye sirf **ek dafa** karna hai.

1. `nexora-test-v6.zip` wali file **download** karein.
2. Usay **extract (unzip)** karein — file par right-click →
   "Extract All". Ek naya folder ban jayega.
3. **Python ek dafa install karein** (free hai):
   - Browser mein **python.org** kholein aur Python download karein.
   - Install shuru karein.
   - ⚠️ Pehli install screen par neeche wala box
     **"Add python.exe to PATH"** lazmi tick karein — ye bohat
     zaroori hai.
   - Install mukammal karein.
4. Nexora wale folder mein jayein aur **`run_nexora.bat`** par
   **double-click** karein.
   - Pehli dafa Nexora apni chhoti free libraries khud install
     karega (1–2 minute, internet chahiye).
   - Phir Nexora ki window khul jayegi. Ho gaya!

## Nexora kaise istemaal karein

1. Window ke upar wali list se **apni zuban chunein**.
2. **Baray neelay button par click karein: 🎤 Speak.**
   - Agar Windows mic ki permission mange to **Allow** karein.
3. **Ek command bolein** — ahista aur saaf awaaz mein.
4. **Nexora kaam kar dega** aur aap ki zuban mein jawab dega.

Mic nahi hai? Koi baat nahi. Command box mein **likh** kar
**Do It** daba dein — wohi kaam ho jayega.

Samajh na aye to Nexora ke andar **❓ Help / How to Use** wala
button dabayein — program ke andar hi sab dobara samjhaya gaya hai.

## Misal wale commands

Ye bolein ya likhein:

| Aap bolein | Nexora karega |
|---|---|
| "open Word" | Microsoft Word khol dega |
| "open YouTube" | YouTube khol dega |
| "search Google for cats" | Google par *cats* search karega |
| "search YouTube for songs" | YouTube par *songs* search karega |
| "type hello, my name is Ahmad" | Aap ke alfaaz type kar dega |
| "what time is it" | Time bata dega |
| "volume up" | Awaaz tez kar dega |

**"Type" wali baat:** "type …" bolne ke baad Nexora 3 second
rukta hai. Jaldi se Word ya Notepad ki window par click karein —
aap ke alfaaz wahan likhay aa jayenge.

## Chhoti pareshaniyon ka hal

**Nexora meri awaaz nahi sun raha / samajh nahi raha**

- Apna **internet** check karein — awaaz sirf online chalti hai.
- Apna **mic** check karein — laga hua hai? on hai?
- **Mic ki permission** check karein — Windows Settings → Privacy →
  Microphone → apps ko microphone istemaal ki ijazat dein.
- Ahista, saaf aur mic ke qareeb bolein.
- Phir bhi na chale? Command **likh** kar **Do It** daba dein.

**"Python is not found" / `run_nexora.bat` nahi chal raha**

- Python install nahi hua, ya PATH wala box tick nahi hua tha.
- Python ko **python.org** se dobara install karein aur is dafa
  pehli screen par **"Add python.exe to PATH"** lazmi tick karein.
- Phir `run_nexora.bat` dobara double-click karein.

**Koi program nahi khul raha (masalan Word)**

- Woh program pehle aap ke laptop par install hona chahiye.
- Agar Word install na ho to Nexora us ki jagah Word ka online
  version browser mein khol deta hai.

## v4 mein naya — hamesha upar rehne wala Nexora icon

Ek chhota sa Nexora "N" wala icon ab laptop ki **har window ke
upar** rehta hai — Word ke upar, Chrome ke upar, har cheez ke upar.

- Usay mouse se **ghaseet kar** screen par kahin bhi le jayein —
  wahi ruk jayega.
- Us par **click** karein (ghaseete baghair) to chhota panel
  khulega: 🎤 **Voice** button, ⌨ **likhne wala box** ✔ button ke
  sath, aur **⌂ Home** button jo Nexora ki bari window samne le
  ayega.
- Panel mein "✕ Hide icon" se chhupa dein, aur bari window ke
  **Floating Icon** button se kabhi bhi wapas le ayen.

**Desktop shortcut (ikhtiyari):** Nexora wale folder mein
`run_nexora.bat` par **right-click → Send to → Desktop (create
shortcut)** karein, phir shortcut par right-click → **Properties →
Change Icon… → Browse…** → **`nexora.ico`** chunein. Bas — ab
desktop par Nexora ka apna "N" wala icon hoga.

## v5 mein naya — hamesha sunna (always-listen) aur naya design

- Nexora ki window ka **naya design** hai: upar logo aur 4
  tasveer wali tiles, **left taraf 4 gol (circle) button** —
  🎤 Voice, 🌐 Language, ❓ Help, 🧭 Floating — aur **right
  taraf** likhne wala box aur guftagu wali jagah (log).
- 🎤 **Voice wala gola button EK dafa dabayein** — us ka ghaira
  **sabz (green)** ho jayega aur Nexora **lagatar sunta rahega**.
  Ab har command ke liye dobara click nahi karna — bas bolte
  jayein, Nexora karta jayega. Band karne ke liye wohi button
  dobara dabayein; Nexora **khud band nahi hota**.
- **Zuban hamesha English se shuru hoti hai.** Badalne ke liye
  🌐 **Language** wala gola button dabayein aur list se zuban
  chunein.
- Ab **"open desktop"**, **"open my computer"** aur **kisi bhi
  app ka naam** ("open Spotify", "open WhatsApp") bhi chalta
  hai — Nexora laptop mein woh app dhoond kar khol deta hai.
  App na mile to saaf keh deta hai, aur kuch ghalat nahi khulta.

---

## v6 mein naya — chhote command, drives, do khane

- **Bas chhota sa command kaafi hai** — pura jumla kehne ki
  zaroorat nahi: sirf **"desktop"**, **"documents"** ya
  **"music"** kahein, Nexora khol dega.
- **Ghalat suna hua lafz khud theek ho jata hai** — mic
  **"destop"** sune to Nexora **"desktop"** samajhta hai.
- **Drive bhi khulti hai:** **"open C drive"** kahein (koi
  bhi letter chalega).
- **Do khane, sath sath:** LEFT wala khaana dikhata hai jo
  **aap ne kaha**, RIGHT wala khaana dikhata hai jo
  **Nexora ne kiya** — ab dono baatein alag alag hain.
- **4 tasveerein ab window ka background** hain (halki
  andheri), upar solid likhai wale khane — aur poori
  window ab chhoti laptop screen (1366×768) par bhi poori
  nazar aati hai, kuch kata hua nahi.
- **Screen poori tarah aap ki zuban mein:** zuban chunein
  to har label aur paighaam usi zuban mein ho jata hai.
  English chunein to screen khalis English hoti hai.

---

*Nexora — Test Version v6 • Free (Rs 0) • Voice works online — internet must be ON.*
