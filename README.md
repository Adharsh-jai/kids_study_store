# 🎓 Spin & Study Tracker

> A gamified, Pomodoro-style study session management web app inspired by the **Google Stitch "Playful Scholar"** design system.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightblue?logo=sqlite)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38BDF8?logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Screenshots](#-screenshots)
4. [Tech Stack](#-tech-stack)
5. [Architecture](#-architecture)
6. [Project Structure](#-project-structure)
7. [Database Design](#-database-design)
8. [API Reference](#-api-reference)
9. [Installation & Setup](#-installation--setup)
10. [Usage Guide](#-usage-guide)
11. [Production Readiness](#-production-readiness)
12. [Future Enhancements](#-future-enhancements)
13. [Project Report](#-project-report)

---

## 📖 Project Overview

**Spin & Study Tracker** is a full-stack web application designed to help students manage and gamify their study sessions. The app combines a task management system with two interactive study tools — a subject spin wheel and a focus timer — to make studying more engaging and structured.

The UI is built faithful to the **Google Stitch "Playful Scholar"** design system: bubbly, high-contrast, rounded components with vibrant yellow, blue, and green accents across a clean off-white background.

---

## ✨ Features

### 🏠 Home Dashboard
- Personalized greeting card with motivational text
- Real-time statistics: Total Sessions · Completed · Minutes Studied · Unique Subjects
- Quick-action buttons to navigate to Spin Wheel and Focus Timer

### 🗺️ My Adventures (Study Sessions — Full CRUD)
- **Create** — Add new study sessions via a modal form
- **Read** — View all sessions as interactive cards with subject icon, status badge, and progress bar
- **Update** — Edit any session's subject, date, duration, status, and notes
- **Delete** — Remove sessions with confirmation dialog
- **Search** — Live debounced text search across subject and notes
- **Filter** — Filter by status: Pending / In Progress / Completed

### 🎡 Daily Spin Wheel
- Animated CSS-based spin wheel with 6 subject segments
- Random subject selection with smooth cubic-bezier animation
- Result card with options to **Log Session** or **Start Timer** for that subject

### ⏱️ Focus Timer (Pomodoro)
- SVG ring countdown timer with animated `stroke-dashoffset`
- Preset durations: **10 / 25 / 45 / 60 minutes**
- Ring color transitions: Yellow → Blue → Red as time runs out
- **Start / Pause / Resume / Reset / Done** controls
- "Done" button auto-prefills the session log modal with subject and duration

---

## 📸 Screenshots

| Page | Description |
|------|-------------|
| 🏠 Home | Dashboard with stats grid and quick actions |
| 🗺️ Adventures | Card-based session grid with CRUD controls |
| 🎡 Spin | Animated multi-segment spin wheel |
| ⏱️ Timer | SVG ring Pomodoro timer with controls |

> All 4 pages are part of a Single Page Application (SPA) — no page reloads.

---

## 🛠️ Tech Stack

### Frontend (Presentation Tier)

| Technology | Version | Role |
|-----------|---------|------|
| HTML5 | — | Semantic page structure |
| Tailwind CSS | 3.x (CDN) | Utility-first styling with custom design tokens |
| Vanilla JavaScript | ES2022 | SPA routing, API calls via `fetch()`, DOM manipulation |
| Google Material Symbols | Latest (CDN) | Icon system matching the Stitch design language |
| Google Fonts | — | Plus Jakarta Sans · Quicksand · Rubik |

### Backend (Logic Tier)

| Technology | Version | Role |
|-----------|---------|------|
| Python | 3.12 | Primary server language |
| Flask | 3.0.3 | Lightweight REST API micro-framework |
| Flask-CORS | 6.0.1 | Cross-Origin Resource Sharing headers |
| Werkzeug | 3.0.3 | WSGI dev server (built into Flask) |

### Database (Data Tier)

| Technology | Version | Role |
|-----------|---------|------|
| SQLite | 3 | Embedded relational database |
| `sqlite3` | stdlib | Python built-in database driver (no ORM) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                                                                 │
│   ┌───────────────────────────────────────────────────────┐     │
│   │              index.html  (SPA — 4 pages)              │     │
│   │   Home  │  Adventures  │  Spin Wheel  │  Focus Timer  │     │
│   └────────────────────┬──────────────────────────────────┘     │
│                        │  HTTP  fetch() REST calls              │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼  localhost:5000
┌─────────────────────────────────────────────────────────────────┐
│                   Flask Application (app.py)                    │
│                                                                 │
│   GET /            →  Serves index.html                         │
│   GET /api/stats   →  Aggregated statistics                     │
│   GET /api/sessions          →  List all (search + filter)      │
│   GET /api/sessions/<id>     →  Single session                  │
│   POST /api/sessions         →  Create session                  │
│   PUT /api/sessions/<id>     →  Update session                  │
│   DELETE /api/sessions/<id>  →  Delete session                  │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │  Python sqlite3
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SQLite Database                               │
│                   study_tracker.db  (local file)               │
│                                                                 │
│   TABLE: sessions                                               │
│   id · subject · duration · notes · status · date · created_at  │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Type

This is a **logically three-tier** application:
- **Tier 1 – Presentation**: `index.html` rendered in the browser
- **Tier 2 – Application/Logic**: Flask REST API in `app.py`
- **Tier 3 – Data**: SQLite database in `study_tracker.db`

However, it is deployed as a **monolith** — Flask serves both the static HTML frontend and the REST API from a single process on one port.

---

## 📁 Project Structure

```
Luxe-store/
│
├── app.py                  # Flask backend — REST API + DB logic
├── index.html              # Frontend SPA — all 4 pages in one file
├── requirements.txt        # Python dependencies
├── study_tracker.db        # SQLite database (auto-created on first run)
└── README.md               # This file
```

---

## 🗄️ Database Design

### Table: `sessions`

```sql
CREATE TABLE sessions (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    subject     TEXT     NOT NULL,
    duration    INTEGER  NOT NULL DEFAULT 25,   -- minutes
    notes       TEXT     DEFAULT '',
    status      TEXT     NOT NULL DEFAULT 'Pending',
    date        TEXT     NOT NULL,              -- YYYY-MM-DD
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Status Values (Enum-like)

| Value | Meaning |
|-------|---------|
| `Pending` | Session planned but not started |
| `In Progress` | Session currently active |
| `Completed` | Session finished |

### Seed Data (auto-inserted on first run)

The app automatically seeds 5 example sessions when the database is first created, so the UI is never empty on first launch.

### Why SQLite?

| Reason | Detail |
|--------|--------|
| ✅ Zero configuration | No separate DB server process needed |
| ✅ Built into Python | `sqlite3` is part of the standard library |
| ✅ Portable | Entire database is a single `.db` file |
| ✅ Sufficient for this scale | Personal study tracker; low concurrency |
| ✅ Fast prototyping | No schema migration tool required |

---

## 📡 API Reference

**Base URL:** `http://127.0.0.1:5000/api`

### Sessions

#### `GET /sessions`
Returns all sessions. Supports query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Filter by subject or notes (partial match) |
| `status` | string | Filter by `Pending`, `In Progress`, or `Completed` |

**Response:**
```json
[
  {
    "id": 1,
    "subject": "Mathematics",
    "duration": 45,
    "notes": "Quadratic equations practice",
    "status": "Completed",
    "date": "2026-08-31",
    "created_at": "2026-08-31T03:58:00"
  }
]
```

#### `GET /sessions/<id>`
Returns a single session by ID.

#### `POST /sessions`
Creates a new session.

**Request body:**
```json
{
  "subject": "Science",
  "duration": 30,
  "notes": "Chapter 3",
  "status": "Pending",
  "date": "2026-08-31"
}
```

**Response:** `201 Created` with the new session object.

#### `PUT /sessions/<id>`
Updates an existing session (partial update supported — only send fields to change).

**Response:** `200 OK` with the updated session object.

#### `DELETE /sessions/<id>`
Deletes a session.

**Response:**
```json
{ "message": "Session deleted" }
```

### Stats

#### `GET /stats`
Returns aggregated statistics.

**Response:**
```json
{
  "total": 5,
  "completed": 3,
  "minutes": 130,
  "subjects": 4
}
```

### Error Responses

| HTTP Code | Meaning |
|-----------|---------|
| `400` | Bad request — missing required fields |
| `404` | Session not found |
| `500` | Internal server error |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone / navigate to the project directory
cd Luxe-store

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

### Open in Browser

```
http://127.0.0.1:5000
```

The SQLite database (`study_tracker.db`) and seed data are created automatically on first run.

---

## 📖 Usage Guide

### Adding a Study Session
1. Navigate to **Adventures** (Tasks tab in bottom nav)
2. Click **"+ New"** button (top right)
3. Fill in Subject, Date, Duration, Status, and Notes
4. Click **"💾 Save"**

### Using the Spin Wheel
1. Navigate to **Spin** tab
2. Click **"SPIN!"** button
3. Wait for the wheel to land on a subject
4. Click **"➕ Log Session"** to log it, or **"⏱ Start Timer"** to time it

### Using the Focus Timer
1. Navigate to **Timer** tab
2. Select a duration preset (10 / 25 / 45 / 60 min)
3. Click **"▶ Start"** to begin countdown
4. Use **Pause / Resume / Reset** as needed
5. Click **"✅ Done"** to auto-log the session

---

## ⚠️ Production Readiness

> **This app is optimised for development and demonstration. It is NOT production-ready out of the box.**

### What Needs to Change for Production

| Area | Issue | Solution |
|------|-------|----------|
| Web server | Werkzeug dev server (`debug=True`) | Use **Gunicorn**: `gunicorn -w 4 app:app` |
| Database | SQLite — single file, no write concurrency | Migrate to **PostgreSQL** with SQLAlchemy |
| Security | No authentication or authorization | Add **Flask-Login** or **JWT** (PyJWT) |
| HTTPS | HTTP only | Put **Nginx** in front with Let's Encrypt SSL |
| CORS | Wildcard `*` origin | Restrict to specific production domain |
| Config | Hardcoded DB path, debug mode | Use `.env` + **python-dotenv** |
| Frontend | Tailwind via CDN (no tree-shaking) | Use **Tailwind CLI** to purge unused classes |
| Logging | Print statements / default Flask logs | Use Python `logging` module + file rotation |

### Deployment Options

#### Option 1 — PaaS (Recommended — Easiest)
Platforms: **Railway**, **Render**, **Fly.io**

```bash
# Switch DB to PostgreSQL first, then:
railway up
```

> ⚠️ SQLite files are wiped on redeploy on most PaaS platforms. Use managed PostgreSQL.

#### Option 2 — VM / VPS (AWS EC2, GCP, DigitalOcean)

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app
# Configure Nginx reverse proxy → port 8000
```

#### Option 3 — Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
```

---

## 🔮 Future Enhancements

| Feature | Priority | Notes |
|---------|----------|-------|
| User authentication (login/signup) | 🔴 High | Required before any multi-user deployment |
| PostgreSQL migration | 🔴 High | Required for production |
| Streak tracking (daily study streaks) | 🟡 Medium | Like Duolingo — gamification boost |
| Subject management (add/edit subjects on wheel) | 🟡 Medium | Currently hardcoded 6 subjects |
| Charts & analytics page | 🟡 Medium | Weekly/monthly study time graphs |
| Push / browser notifications | 🟢 Low | Timer completion alerts |
| Dark mode toggle | 🟢 Low | Design system supports dark tokens |
| Export to CSV / PDF | 🟢 Low | Session history export |
| Mobile PWA support | 🟢 Low | Installable on phone home screen |

---

## 📋 Project Report

### Project Title
**Spin & Study Tracker** — A Gamified Study Session Manager

### Objective
To design and develop a full-stack web application that helps students organise, track, and gamify their study sessions using modern web technologies, while maintaining a visually engaging and intuitive user interface inspired by the Google Stitch "Playful Scholar" design system.

### Problem Statement
Students often struggle with:
1. Lack of structure in study planning
2. Decision fatigue — not knowing what subject to study next
3. Poor time management during study sessions
4. No visibility into study patterns and progress

### Solution
A three-component web app:
1. **Study Session CRUD** — log and track every session with status, duration, and notes
2. **Spin Wheel** — eliminate decision fatigue by randomly selecting a subject
3. **Focus Timer** — enforce structured Pomodoro-style focus sessions with visual feedback

### Development Approach
- **Design-First**: The UI was reverse-engineered from actual Google Stitch screen exports, ensuring pixel-level accuracy to the Playful Scholar design system
- **API-First Backend**: Flask routes were designed as a clean REST API before the frontend was connected, making future decoupling easy
- **Single-File Frontend**: The entire 4-page SPA was kept in one HTML file to simplify deployment (no build step, no bundler)

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| SQLite over PostgreSQL | Zero-config setup; appropriate for a personal-use app at this stage |
| Vanilla JS over React/Vue | No build toolchain needed; simpler deployment; sufficient for this scale |
| Tailwind CDN over CLI build | Rapid prototyping priority; eliminates build step for demo purposes |
| SPA (single HTML file) | No routing library needed; Flask serves one file; all navigation is CSS-driven |
| Flask over Django | Microframework is more appropriate for a small REST API; less boilerplate |

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Delete button not working (original) | Fixed CORS and `fetch()` method configuration; ensured correct HTTP `DELETE` verb |
| Matching the Stitch design exactly | Downloaded and parsed all 4 Stitch screen HTML exports to extract exact tokens, components, and patterns |
| Spin wheel accuracy | Implemented modular angle math with cubic-bezier easing to ensure the pointer always lands on the correct segment |
| Timer ring animation | Used SVG `stroke-dashoffset` with `stroke-dasharray: 880` (circumference of r=140 circle) for smooth countdown |
| Auto-logging from Timer | "Done" button reads the elapsed duration and pre-fills the session modal before navigating to the Adventures page |

### Testing

| Test Type | Method |
|-----------|--------|
| API Testing | Manual testing via browser `fetch()` calls and Flask debug logs |
| UI Testing | Manual browser testing across Chrome and Edge |
| CRUD Verification | Verified all 5 operations (Create, Read-all, Read-one, Update, Delete) via network tab |

### Results
- Fully functional 4-page SPA with real-time data from a REST API
- All CRUD operations working correctly with proper HTTP status codes
- Animated spin wheel with 6 segments and result-to-session workflow
- Pomodoro timer with live countdown, ring animation, and auto-session logging
- Responsive layout working on both desktop and mobile viewports

### Conclusion
The Spin & Study Tracker successfully demonstrates a complete full-stack web application with a professional, design-system-consistent UI. While the current stack is optimised for development speed and simplicity, a clear upgrade path to production exists through Gunicorn, PostgreSQL, Nginx, and authentication middleware.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ using Python · Flask · SQLite · Tailwind CSS · Google Stitch Design System*
