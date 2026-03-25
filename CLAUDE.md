# Mirror Companion App — Master Project Plan v2
*A growing companion for your daughter, powered by Raspberry Pi 5*
*Last updated: After hardware research + project structure review*

---

## ⚡ How to Use This Document

**Paste this document at the start of every Claude coding session.**
Then say: *"I'm working on [Phase X / Backlog item Y]. Here's what's already working: [status]."*

Claude will have full context instantly — no re-explaining. This document IS the memory.

---

## Hardware Stack (Verified)

| Component | Item | Status |
|---|---|---|
| Computer | Raspberry Pi 5 | ✅ Great choice |
| Display | Your monitor (HDMI) | ✅ |
| Camera | Pi Camera | ✅ (Phase 4+) |
| Speaker | USB mini soundbar (B086JXJ1LF) | ✅ Works on Linux |
| Microphone | **CMTECK B07C2YX4T1** | ❌ NOT Linux compatible — must replace |
| Mic (recommended) | **ReSpeaker USB Mic Array v2.0** | ✅ Purpose-built for voice assistants |
| Mic (budget alt) | Any USB mic labeled "UAC compliant" | ✅ |

**Action required before Phase 1:** Order a replacement microphone.
The CMTECK uses a proprietary chip with no Linux drivers. It will not work on Pi OS.

---

## Tech Stack (Verified + Optimized)

| Layer | Technology | Notes |
|---|---|---|
| OS | Raspberry Pi OS 64-bit (Bookworm) | Current stable release |
| Display | Chromium in kiosk mode | Auto-launch on boot |
| Frontend | React (Vite, served locally) | Vite is faster than CRA on Pi |
| Backend | Python 3.11 + FastAPI | Lightweight, async-friendly |
| Wake word | Picovoice Porcupine | "Mirror Mirror" — Pi 5 confirmed |
| Speech-to-text | OpenAI Whisper API | Already have key |
| AI brain | OpenAI GPT-4o-mini | Fast, cheap, child-safe prompting |
| Text-to-speech | OpenAI TTS (nova voice) | Warm, friendly — best for children |
| Character animation | SVG + CSS animations in React | No GPU needed, smooth on Pi 5 |
| Database | SQLite via Python (aiosqlite) | Local, no server required |
| Parent dashboard | React (same app, route /dashboard) | Access at http://[pi-ip]:8080 |
| Process manager | systemd | Auto-restart on crash, starts on boot |

---

## App Overview

A voice-only companion app running on a Raspberry Pi 5 behind a two-way magic mirror.
An animated character lives in the mirror. The child names it and talks to it by voice.
The app grows with her — starting as a playful friend at age 3, evolving to include
chore tracking, morning routines, and eventually a calendar and life assistant.
Parents manage everything from a web browser on their phone or laptop (same WiFi).

**Core feeling:** *"My best friend lives in the mirror and she knows me."*

---

## Code Structure

Every session with Claude will use this folder structure. Keep it consistent.

```
mirror-companion/
├── README.md                  ← paste project plan here too
├── .env                       ← API keys (never commit to git)
├── .gitignore
│
├── backend/                   ← Python / FastAPI
│   ├── main.py                ← app entry point
│   ├── routes/
│   │   ├── voice.py           ← speech endpoints
│   │   ├── character.py       ← character/identity
│   │   ├── chores.py          ← chore management
│   │   └── dashboard.py       ← parent dashboard API
│   ├── services/
│   │   ├── openai_service.py  ← Whisper, GPT, TTS calls
│   │   ├── wake_word.py       ← Porcupine listener
│   │   └── audio.py           ← mic/speaker management
│   ├── models/
│   │   └── database.py        ← SQLite schema + queries
│   └── requirements.txt
│
├── frontend/                  ← React / Vite
│   ├── src/
│   │   ├── App.jsx            ← root, routes
│   │   ├── pages/
│   │   │   ├── Mirror.jsx     ← main mirror display
│   │   │   └── Dashboard.jsx  ← parent web app
│   │   ├── components/
│   │   │   ├── Character/     ← SVG character + animations
│   │   │   ├── ListeningWave/ ← audio visualizer
│   │   │   └── Clock/         ← idle clock display
│   │   └── hooks/
│   │       └── useVoice.js    ← voice state management
│   └── package.json
│
├── wake-word/
│   └── mirror-mirror-pi5.ppn  ← trained Porcupine model file
│
└── systemd/
    ├── mirror-backend.service ← auto-start backend on boot
    └── mirror-frontend.service← auto-start Chromium kiosk
```

---

## How Coding Sessions Work With Claude

### Starting a Session

Copy/paste this template at the top of every new Claude conversation:

```
PROJECT: Mirror Companion App (Raspberry Pi 5 magic mirror for my daughter)

PLAN DOC: [paste this full document]

TODAY'S GOAL: [one specific thing, e.g. "Build the FastAPI backend skeleton with a /speak endpoint"]

CURRENT STATUS:
- What's working: [e.g. "Pi is set up, Chromium kiosk mode is running"]
- What's broken: [e.g. "Audio playback has a 2 second delay"]
- Last thing we did: [e.g. "Got Porcupine detecting wake word successfully"]

BLOCKER/QUESTION: [optional — anything specific you're stuck on]
```

### Rules for Good Sessions

- **One goal per session.** "Get the wake word working" is a great session goal. "Build the whole voice pipeline" is too big.
- **Paste errors in full.** When something breaks, paste the entire error output — not a summary of it.
- **Tell Claude what you tried.** "I already tried restarting the service" saves time.
- **End sessions with a status update.** Before closing, note what's working so next session's "current status" is accurate.

### When Claude Gives You Code

- Claude will write complete, runnable files — not snippets
- Test each piece before moving on
- If something doesn't work, paste the exact error back and say "this didn't work, here's the error"
- Don't try to fix Claude's code manually unless you understand what it's doing — just report back

---

## Backlog Approach (Not Everything Upfront)

The project is organized into **Phases** (required, in order) and a **Backlog** (ideas to draw from).

You do NOT need to plan the backlog in detail now. As you build and have ideas,
drop them in the backlog. When a phase is done, look at the backlog and pick what's next.

---

## Build Phases (Required, In Order)

### ✅ Phase 0 — Hardware Setup
*Do this before any code*

- [ ] Order ReSpeaker USB Mic Array v2.0 (or UAC-compliant USB mic)
- [ ] Install Raspberry Pi OS Bookworm 64-bit on SD card
- [ ] Connect display, speaker, microphone
- [ ] Verify Pi boots and connects to WiFi
- [ ] Enable SSH for remote work from laptop
- [ ] Test microphone: `arecord -l` (should list your mic)
- [ ] Test speaker: `speaker-test -t wav`
- [ ] Train "Mirror Mirror" wake word on Picovoice Console (select Raspberry Pi platform)
- [ ] Download the .ppn file → put in wake-word/ folder

**Milestone:** Pi boots, microphone and speaker work, .ppn file is ready.

---

### Phase 1 — Foundation (Voice Pipeline)
*Goal: Pi hears "Mirror Mirror" and speaks back*

1. Set up project folder structure
2. Install dependencies (Python, Node.js 20, Vite)
3. Build bare React app — black screen, centered glowing circle
4. Configure Chromium kiosk mode (auto-launch on boot)
5. Build FastAPI backend with `/speak` and `/listen` endpoints
6. Wire Porcupine wake word listener (runs as background service)
7. Record audio after wake word (VAD — voice activity detection)
8. Send audio → OpenAI Whisper → get text
9. Send text → GPT-4o-mini → get response
10. Send response → OpenAI TTS → play audio back
11. Wire it all together end-to-end

**Milestone:** Say "Mirror Mirror, what's your favorite color?" and hear a reply.

---

### Phase 2 — Character System
*Goal: A named, animated companion lives in the mirror*

1. Design 4 character options as SVG (simple animals/creatures)
2. Build animation states: idle (breathing), listening, talking, happy, sleepy
3. Build first-run setup flow — voice-guided character selection and naming
4. Save character choice + name to SQLite
5. Load character personality into GPT system prompt
6. Character uses child's name in conversation
7. Character remembers what they talked about in the same session

**Milestone:** She picks a character, names it, and it greets her by name the next day.

---

### Phase 3 — Companion AI
*Goal: Genuinely fun and age-appropriate friend*

1. Build persistent memory (interests, birthday, recent topics)
2. Tune GPT prompt for 3-year-old language (short sentences, playful, encouraging)
3. Add mini-games: jokes, animal sounds, colors, counting, "I Spy"
4. Add storytime mode ("Tell me a story about a dragon")
5. Add emotional awareness (if she sounds sad → character responds warmly)
6. Add idle behaviors (character "falls asleep" after 10 mins, wakes when she talks)

**Milestone:** 15-minute play session feels natural, fun, and age-appropriate.

---

### Phase 4 — Parent Dashboard
*Goal: Manage everything from your phone*

1. Build React dashboard at /dashboard
2. Child profile page (name, age, interests, birthday)
3. Character settings (name, voice, personality notes)
4. Conversation log viewer (browse last 7 days)
5. Settings (volume, sleep schedule, wake word sensitivity)
6. Simple PIN lock to prevent child from changing settings

**Milestone:** Update child's age and interests from phone; mirror reflects them next conversation.

---

### Phase 5 — Routines + Chores
*Goal: Morning routine and chore tracking*

1. Chore manager in dashboard (add/edit/delete chores, set frequency)
2. Mirror announces chores in morning ("Good morning! You have 2 things today")
3. Voice-guided chore check-off ("I cleaned my room!" → "Amazing! Check!")
4. Celebration moments (streak tracking, character does a happy dance)
5. Morning routine mode (triggered at set time — weather, day of week, checklist)
6. Reminder system (configurable reminder times via dashboard)

**Milestone:** One full week of morning routine + chore tracking working reliably.

---

## Backlog (Ideas — No Order, No Urgency)

Add to this as inspiration strikes. Pull from it when a phase is done.

### Character & Personality
- [ ] Character birthday (she can say happy birthday to it)
- [ ] Character changes appearance for holidays (little Santa hat, bunny ears)
- [ ] Character has "moods" that affect its dialogue style
- [ ] Multiple characters she can switch between (unlock a new one for a milestone)
- [ ] She can teach the character new things ("My favorite color is purple")

### Games & Learning
- [ ] Spelling helper (she says a word, character spells it out)
- [ ] Math practice mode (age-appropriate as she grows)
- [ ] "Guess the animal" sound game
- [ ] Weather report ("What's the weather today?")
- [ ] Knock knock joke database

### Routines & Life
- [ ] Bedtime routine mode (wind-down stories, breathing exercises)
- [ ] Calendar view for birthdays and events (visible on idle screen)
- [ ] Homework help mode (age 6+)
- [ ] Medication/vitamin reminders (for parents to configure)
- [ ] "How are you feeling today?" check-in with emoji/color picker

### Magic Mirror Display
- [ ] Ambient clock on idle screen (soft, not distracting)
- [ ] Weather widget on idle screen
- [ ] Pi Camera integration — character "sees" her and waves
- [ ] Her photo of the week visible on idle screen (parent uploads from dashboard)
- [ ] Digital sticker collection (earned for chores/routines)

### Technical Improvements
- [ ] Offline fallback mode (canned responses if internet drops)
- [ ] Voice volume auto-adjust based on background noise
- [ ] Multiple child profiles (if a sibling comes along)
- [ ] Export conversation logs to email (weekly summary for parent)
- [ ] GitHub Actions for easy updates (push → auto-deploy to Pi)

---

## Environment Variables (.env file — never commit)

```
OPENAI_API_KEY=your_key_here
PICOVOICE_ACCESS_KEY=your_key_here
DASHBOARD_PIN=1234
CHILD_NAME=your_daughters_name
```

---

## Open Questions (Decide When You're Ready)

- [ ] What are the 4 character options? (fox, bunny, dragon, cat? Something she already loves?)
- [ ] Should idle screen show a clock? Weather?
- [ ] What time does the mirror "go to sleep" and stop listening?
- [ ] Should the Pi Camera be used now (Phase 1) or later?

---

## Current Status Log

Use this section to track what's done as you build.

| Date | Phase | What Was Completed |
|---|---|---|
| — | 0 | Planning only — no code yet |

---

*This is a living document. Update the status log and open questions as you go.*
*The more current this doc is, the more effectively Claude can help each session.*
