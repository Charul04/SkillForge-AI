# ⚡ SkillForge AI

> **CULTIVATE SKILLS. GROW YOUR FUTURE.**

An intelligent, gamified career development platform that predicts your best-fit tech career, builds a personalized roadmap, and keeps you accountable — all in one app.

**Made by Charul Sahu** | Hackathon Project 2025

---

## 🚀 Live Demo

```bash
streamlit run app.py
```

---

## 📸 Preview

| Prediction + Radar | Roadmap + YouTube Links |
|---|---|
| AI predicts your career with readiness score | 10-step ordered roadmap, one resource per task |

| Skill Challenge Quiz | Smart Scheduler |
|---|---|
| 25 MCQ flashcards per career, earn XP | Auto week-by-week calendar from your hours |

---

## ✨ Features

### 🎯 AI Career Prediction
- Rate yourself on **10 skills** (Python, SQL, ML, Web Dev, UI/UX, Communication, Problem Solving, Cloud, Data Analysis, Cybersecurity) using interactive sliders (0–10)
- scikit-learn ML model instantly predicts your **best-fit career** from 9 career paths
- Visual **Career Readiness score** shown as a progress bar
- Live **Skill Radar chart** (Plotly) updates as you move sliders
- Horizontal **skill profile bars** showing all 10 skill scores at a glance

### 🗺️ Personalized Career Roadmap
- **10-step ordered roadmap** for each of 9 career paths
- Every checkpoint has a **YouTube resource link** directly to the best free tutorial
- Check off tasks as you complete them — **progress saves to your profile**
- XP bar updates in real time — **200 XP = 100% roadmap completion**
- Download your roadmap progress as part of the PDF report

### 🎮 Skill Challenge Mode
- **25 hand-written MCQ questions** per career (225 questions total across all 9 careers)
- Questions are **randomized every session** for fresh experience
- Flashcard-style: click A/B/C/D → instant **green ✅ / red ❌ feedback**
- **+5 XP per correct answer** — bonus XP saved to your profile
- Live score tracker: Questions answered, XP earned, Accuracy %
- Final results screen with grade: 🏆 Excellent / 👍 Good / 📚 Keep Learning

### 📅 Smart Scheduler
- Input your **available hours per week** → app auto-generates a week-by-week task calendar
- Each task has a **hardcoded estimated duration** (3–10 hours based on complexity)
- Calendar view shows colour-coded weekly load bars (green = manageable, amber = full, red = overloaded)
- Each scheduled task shows the **YouTube link** and time estimate inline
- Completed tasks marked ✅, pending tasks marked 📌
- **Download your schedule** as a `.txt` file
- Stats panel: Total pending hours, weeks needed, tasks remaining

### 🏆 Community Leaderboard
- Real-time leaderboard showing **all registered users** ranked by XP
- Displays: Career path, Level, XP score (capped at 200), Streak
- Your own entry highlighted separately as **(you)**
- Medal emojis for top 3 positions 🥇🥈🥉

### ⭐ XP & Gamification System
- **XP = (Roadmap Progress % / 100) × 200** — always consistent with actual progress
- **Level system**: Level 1 → Level 2 as XP grows to 200
- **Daily streak tracker**: Fire emoji 🔥 shows consecutive days active
- Sidebar shows XP bar, streak pill, and level badge in real time
- Skill Challenge awards **bonus XP** on top of roadmap XP

### 📄 Export / PDF Report
- One-click **PDF report generation** using FPDF2
- Report includes: Username, Career Path, Level, XP, Streak, Progress %, all 10 skill scores, full roadmap checklist
- Unicode-safe: all special characters sanitized for PDF compatibility
- Download directly from the Export tab

### 💬 AI Chatbot (Chatbase)
- **24/7 career support chatbot** embedded as a floating widget in the bottom-right corner
- Appears **only after authentication** — not visible on the login/register screen
- Powered by **Chatbase** (bot ID: `Sl0q4y9ILFqIdK8szW1Gv`)
- Injected via `streamlit.components.v1` for proper script execution

### 🔐 Authentication System
- Secure **username + password** registration and login
- Passwords hashed with **SHA-256** before storage
- **SQLite WAL mode** for concurrent access without locking
- Auto-migration: existing databases upgraded without data loss
- Session state preserves login across Streamlit reruns

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit, Custom CSS (dark glassmorphism theme) |
| **ML Model** | scikit-learn (RandomForestClassifier / trained model) |
| **Data Visualization** | Plotly (Radar chart, Bar charts) |
| **Database** | SQLite with WAL mode |
| **PDF Generation** | FPDF2 |
| **AI Chatbot** | Chatbase (embedded widget) |
| **Script Injection** | streamlit.components.v1 |
| **Language** | Python 3.10+ |

---

## 🎓 Supported Career Paths

| # | Career | Key Skills |
|---|---|---|
| 1 | 🔬 Data Scientist | Python, Pandas, ML, Statistics, Visualization |
| 2 | 🤖 ML Engineer | Deep Learning, MLOps, Docker, PyTorch |
| 3 | 🌐 Frontend Developer | React, CSS, JavaScript, TypeScript |
| 4 | ⚙️ Backend Developer | APIs, Databases, Docker, Redis |
| 5 | 🎨 UI/UX Designer | Figma, User Research, Prototyping |
| 6 | 🔒 Cybersecurity Analyst | Networking, Ethical Hacking, SIEM |
| 7 | 💻 Software Engineer | DSA, System Design, OOP, Git |
| 8 | ☁️ Cloud Engineer | AWS/GCP/Azure, Kubernetes, Terraform |
| 9 | 🔄 DevOps Engineer | CI/CD, Docker, Ansible, Monitoring |

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourname/skillforge-ai.git
cd skillforge-ai

# Install dependencies
pip install streamlit scikit-learn plotly fpdf2 pandas numpy requests --break-system-packages

# Run the app
streamlit run app.py
```

### First Run
1. The SQLite database (`skillforge.db`) is created automatically on first launch
2. Register a new account on the **Create Account** tab
3. Start with the **🎯 Prediction** tab — rate your skills and get your career prediction

---

## 📁 Project Structure

```
skillforge-ai/
│
├── app.py                  # Main Streamlit application (single file)
├── skillforge.db           # SQLite database (auto-created)
├── model.pkl               # Trained scikit-learn model
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

---

## 🗃️ Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,          -- SHA-256 hashed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- User stats & progress
CREATE TABLE user_stats (
    username TEXT PRIMARY KEY,
    career TEXT,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    streak INTEGER DEFAULT 0,
    last_login TEXT,
    progress INTEGER DEFAULT 0,      -- Roadmap completion %
    completed_tasks TEXT DEFAULT '[]',
    skill_python INTEGER DEFAULT 5,
    skill_sql INTEGER DEFAULT 5,
    skill_ml INTEGER DEFAULT 5,
    skill_web INTEGER DEFAULT 5,
    skill_uiux INTEGER DEFAULT 5,
    skill_comm INTEGER DEFAULT 5,
    skill_prob INTEGER DEFAULT 5,
    skill_cloud INTEGER DEFAULT 5,
    skill_data INTEGER DEFAULT 5,
    skill_cyber INTEGER DEFAULT 5
);

-- Leaderboard
CREATE TABLE leaderboard (
    username TEXT PRIMARY KEY,
    career TEXT,
    xp INTEGER DEFAULT 0,
    progress INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎮 XP & Leveling System

```
XP = (Roadmap Progress % ÷ 100) × 200

0%   roadmap  →   0 XP   (Level 1)
50%  roadmap  → 100 XP   (Level 1)
100% roadmap  → 200 XP   (Level 2)

Skill Challenge Bonus: +5 XP per correct answer (capped at 200 total)
```

---

## 🧩 Quiz Data Coverage

| Career | Questions |
|---|---|
| Data Scientist | 25 |
| ML Engineer | 25 |
| Frontend Developer | 25 |
| Backend Developer | 25 |
| UI/UX Designer | 25 |
| Cybersecurity Analyst | 25 |
| Software Engineer | 25 |
| Cloud Engineer | 25 |
| DevOps Engineer | 25 |
| **Total** | **225** |

---

## 🔧 Configuration

### Chatbase Widget
The chatbot is configured with bot ID `Sl0q4y9ILFqIdK8szW1Gv`. To use your own bot:
1. Create a bot at [chatbase.co](https://www.chatbase.co)
2. Replace the script ID in `app.py` → `render_app()` function

### Database Path
Default: `skillforge.db` in the same directory as `app.py`. Change `DB_PATH` at the top of `app.py`.

---

## 🐛 Known Issues & Fixes

| Issue | Fix Applied |
|---|---|
| `sqlite3.OperationalError: database is locked` | WAL mode + shared cached connection via `@st.cache_resource` |
| `FPDFUnicodeEncodingException` on PDF export | Unicode sanitizer replaces en-dash, em-dash, emojis with ASCII |
| `StreamlitDuplicateElementId` on Plotly charts | Unique `key=` argument on every `st.plotly_chart()` call |
| `StreamlitDuplicateElementKey` on sliders | Removed duplicate Smart Scheduler tab insertion |
| Chatbase script stripped by Streamlit | Replaced `st.markdown()` with `streamlit.components.v1.html()` targeting `window.parent` |

---

## 📊 App Tabs Overview

| Tab | Description |
|---|---|
| 🎯 Prediction | AI career prediction, skill profile, radar chart |
| 🎮 Skill Challenge | Career-specific MCQ quiz with XP rewards |
| 📅 Smart Scheduler | Auto week-by-week task calendar |
| 🗺️ Roadmap | Ordered tasks with YouTube links and XP tracking |
| 🏆 Leaderboard | Community ranking by XP |
| 📄 Export | Download professional PDF career report |

---

## 👩‍💻 Author

**Charul Sahu**
Hackathon 2025 — SkillForge AI

---

## 📄 License

This project was built for hackathon purposes. All quiz content, roadmap data, and YouTube resource links are curated manually for educational use.

---

*"From lost to launched — that's SkillForge AI."* ⚡
