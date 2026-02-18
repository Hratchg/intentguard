# IntentGuard

> Explainable user-behavior & risk intelligence platform

IntentGuard analyzes user event streams to detect churn risk, fraud patterns, and UX confusion — then explains *why* in plain English and recommends actions.

## Features

- **Churn Early Warning** — Detects declining engagement patterns and recommends interventions
- **Fraud Pattern Detection** — Identifies anomalous behavior using Isolation Forest + feature analysis
- **UX Confusion Detector** — Clusters support tickets and search queries to surface product issues
- **Explainable AI** — Every risk score comes with plain-English reasoning and top contributing factors
- **Interactive Dashboard** — Explore users, timelines, risk scores, and UX clusters in real time

## Use Cases

### Churn Prevention

A product team notices retention is slipping. They open IntentGuard, filter by **churn** scenario, and sort by risk score. For each at-risk user they see:

1. **Risk gauge** — a GradientBoosting score (0–1) trained on engagement patterns
2. **Top factors** — e.g., "session frequency dropped 60 % over 14 days," "last feature use was 9 days ago"
3. **Plain-English explanation** — *"This user's engagement has been steadily declining. They stopped using core features and their sessions are shorter. Consider a re-engagement email or in-app prompt."*

The team exports the high-risk list, hands it to lifecycle marketing, and ships a targeted campaign the same day.

### Fraud Investigation

A security analyst filters by **fraud** scenario. IntentGuard's Isolation Forest flags users whose behavior deviates from the population — no labels required. A flagged profile might show:

- Rapid micro-transactions at 3 AM
- Abnormally short session durations
- Access from an unusual number of device fingerprints

Each flag includes the anomaly score and the features that contributed most, giving the analyst concrete evidence to escalate or dismiss.

### UX Improvement

A PM opens the **Insights → Confusion Clusters** panel. IntentGuard groups support tickets and rage-click sequences by similarity, then auto-generates a summary for each cluster:

- **Cluster: "Checkout address form"** — 12 tickets, common theme: users can't find the "same as billing" checkbox → suggested fix: move checkbox above the form
- **Cluster: "Password reset flow"** — 8 tickets, common theme: confirmation email never arrives → suggested fix: check spam-filter triggers, add resend button

The PM drags the top cluster straight into the next sprint.

## How the ML Works

IntentGuard runs two complementary models plus an explanation engine:

| Component | Technique | Purpose |
|-----------|-----------|---------|
| Churn model | **GradientBoosting** (supervised) | Trained on labeled scenario data to predict disengagement probability |
| Fraud model | **Isolation Forest** (unsupervised) | Detects statistical outliers with no need for labeled fraud examples |
| Explanation engine | Feature-importance + template NLG | Translates top contributing factors into plain-English reasoning |

Both models consume **19 behavioral features** extracted from raw event streams — session frequency, time-of-day distribution, feature adoption breadth, support-ticket sentiment, and more. Every score returned by the API includes the feature-importance vector and a human-readable explanation so downstream teams never see a number without context.

## Dashboard Walkthrough

When you open the app you land on a single-page experience with two main areas:

- **Left sidebar** — Searchable user list with filters for scenario (churn / fraud / confusion) and risk level (low / medium / high). Click any user to load their profile.
- **Right panel** — Risk gauges for each model, a scrollable event timeline, and feature-importance bar charts. Hit *Recalculate* to re-run the ML pipeline live and watch scores update.

Scroll down through the portfolio narrative sections: **Hero → Why → Scenarios → Live Dashboard → Architecture → Tech Stack** — each animated into view with Framer Motion.

## Quick Start

```bash
docker-compose up
```

The demo ships with **50 synthetic users** and pre-trained models — no external data or GPU required.

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

## Development Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Seed Database

```bash
cd data
python seed.py
python train_models.py
```

### Run Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Architecture

```
Events → Session Builder → Feature Extraction → ML Scoring → Explanation → Action
```

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI, Python 3.12+ |
| ML Pipeline | scikit-learn (GradientBoosting, IsolationForest) |
| Database | SQLite via aiosqlite |
| Frontend | React 18, TypeScript, Vite |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Animations | Framer Motion |
| Data Fetching | TanStack Query |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/users` | List users (filter by scenario, risk_level) |
| GET | `/api/users/{id}` | User detail with risk scores |
| GET | `/api/users/{id}/timeline` | Event timeline (paginated) |
| GET | `/api/users/{id}/risk` | Risk scores with explanations |
| POST | `/api/users/{id}/risk/recalculate` | Re-run ML scoring live |
| GET | `/api/insights/clusters` | UX confusion clusters |
| GET | `/api/stats/overview` | Aggregate statistics |

## Project Structure

```
intentguard/
├── backend/           # FastAPI + sklearn
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── models/    # Pydantic schemas
│   │   ├── ml/        # ML pipelines + explanation engine
│   │   └── data/      # SQLite schema + access layer
│   └── tests/
├── frontend/          # React + Vite + TypeScript
│   └── src/
│       ├── api/       # API client + types
│       ├── components/# Reusable UI (gauges, charts, cards)
│       ├── dashboard/ # Interactive dashboard
│       └── sections/  # Portfolio narrative sections
├── data/
│   ├── generators/    # Simulated dataset generators
│   ├── seed.py        # Database seeding script
│   └── train_models.py# Model training + score computation
├── models/            # Trained sklearn pipelines (.pkl)
└── docker-compose.yml
```
