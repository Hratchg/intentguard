# IntentGuard

> Explainable user-behavior & risk intelligence platform

IntentGuard analyzes user event streams to detect churn risk, fraud patterns, and UX confusion — then explains *why* in plain English and recommends actions.

## Features

- **Churn Early Warning** — Detects declining engagement patterns and recommends interventions
- **Fraud Pattern Detection** — Identifies anomalous behavior using Isolation Forest + feature analysis
- **UX Confusion Detector** — Clusters support tickets and search queries to surface product issues
- **Explainable AI** — Every risk score comes with plain-English reasoning and top contributing factors
- **Interactive Dashboard** — Explore users, timelines, risk scores, and UX clusters in real time

## Quick Start

```bash
docker-compose up
```

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
