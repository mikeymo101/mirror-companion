# Mirror Companion

A voice-powered animated companion for your child, running on a Raspberry Pi 5 behind a two-way magic mirror.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) |
| Backend | Python 3.11 + FastAPI |
| Wake Word | Picovoice Porcupine ("Mirror Mirror") |
| Speech-to-Text | OpenAI Whisper API |
| AI | OpenAI GPT-4o-mini |
| Text-to-Speech | OpenAI TTS (nova voice) |
| Display | Chromium kiosk mode |
| Database | SQLite (aiosqlite) |
| Process Manager | systemd |

## Quick Start (Development on Laptop)

### 1. Clone and configure

```bash
git clone <repo-url>
cd mirror-companion
cp .env.example .env
# Edit .env with your API keys
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and the parent dashboard at `http://localhost:5173/dashboard`.

## Quick Start (Raspberry Pi Deployment)

### 1. Set up the project

```bash
cd /home/pi
git clone <repo-url>
cd mirror-companion
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install and start services

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
npm run build

# Install systemd services
sudo cp systemd/mirror-backend.service /etc/systemd/system/
sudo cp systemd/mirror-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mirror-backend mirror-frontend
sudo systemctl start mirror-backend mirror-frontend
```

### 3. Verify

```bash
sudo systemctl status mirror-backend
sudo systemctl status mirror-frontend
```

Access the parent dashboard from any device on the same WiFi at `http://<pi-ip>:5173/dashboard`.

## Project Structure

```
mirror-companion/
├── backend/             # Python / FastAPI backend
│   ├── main.py          # App entry point
│   ├── routes/          # API route handlers
│   ├── services/        # OpenAI, wake word, audio services
│   ├── models/          # SQLite schema + queries
│   └── requirements.txt
├── frontend/            # React / Vite frontend
│   ├── src/
│   │   ├── pages/       # Mirror display + parent dashboard
│   │   ├── components/  # Character, animations, clock
│   │   └── hooks/       # Voice state management
│   └── package.json
├── wake-word/           # Porcupine .ppn model file
├── systemd/             # Service files for Pi auto-start
├── .env.example         # Environment variable template
└── CLAUDE.md            # Full project plan and session guide
```

## Project Plan

See [CLAUDE.md](./CLAUDE.md) for the full project plan, build phases, backlog, and session workflow.
