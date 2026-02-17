# IntentGuard Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a portfolio-ready explainable user-behavior and risk intelligence platform with interactive demo, simulated data, and real ML scoring.

**Architecture:** Python FastAPI backend with sklearn ML pipelines serves a REST API. React + Vite + TypeScript frontend renders a single scrollable page: portfolio narrative sections scroll into an embedded interactive dashboard. SQLite stores simulated event data. Monorepo with docker-compose for one-command setup.

**Tech Stack:** FastAPI, sklearn, aiosqlite, SQLite, React 18, Vite, TypeScript, Tailwind CSS, Recharts, Framer Motion, TanStack Query, Docker

---

## Phase 1: Project Scaffolding

### Task 1: Initialize Git Repo and Root Structure

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Create: `docker-compose.yml`

**Step 1: Initialize the git repo**

```bash
cd "C:/Users/King Hratch/intentguard"
git init
```

**Step 2: Create .gitignore**

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/

# Node
node_modules/
frontend/dist/

# Data
data/intentguard.db
models/*.pkl

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local
```

**Step 3: Create README.md**

```markdown
# IntentGuard

> Explainable user-behavior & risk intelligence platform

IntentGuard analyzes user event streams to detect churn risk, fraud patterns, and UX confusion — then explains *why* in plain English and recommends actions.

## Quick Start

```bash
docker-compose up
```

Frontend: http://localhost:5173
Backend API: http://localhost:8000/docs

## Development

See `docs/plans/` for architecture and design docs.
```

**Step 4: Create placeholder docker-compose.yml**

```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

**Step 5: Commit**

```bash
git add .gitignore README.md docker-compose.yml docs/
git commit -m "chore: initialize repo with root structure and docker-compose"
```

---

### Task 2: Scaffold Backend (FastAPI)

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`
- Create: `backend/Dockerfile`
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/ml/__init__.py`
- Create: `backend/app/data/__init__.py`

**Step 1: Create requirements.txt**

```
fastapi==0.115.6
uvicorn[standard]==0.34.0
aiosqlite==0.20.0
scikit-learn==1.6.1
pandas==2.2.3
numpy==2.2.2
pydantic==2.10.5
python-multipart==0.0.20
```

**Step 2: Create backend/app/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="IntentGuard API",
    description="Explainable user-behavior & risk intelligence",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

**Step 3: Create backend/Dockerfile**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Step 4: Create empty __init__.py files for all subpackages**

Create empty files:
- `backend/app/__init__.py`
- `backend/app/api/__init__.py`
- `backend/app/models/__init__.py`
- `backend/app/ml/__init__.py`
- `backend/app/data/__init__.py`

**Step 5: Verify backend starts**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000 &
curl http://localhost:8000/api/health
# Expected: {"status":"ok"}
kill %1
```

**Step 6: Commit**

```bash
git add backend/
git commit -m "feat: scaffold FastAPI backend with health endpoint"
```

---

### Task 3: Scaffold Frontend (React + Vite + TS + Tailwind)

**Files:**
- Create: `frontend/` (via Vite scaffolding)
- Modify: `frontend/src/App.tsx`
- Create: `frontend/Dockerfile`

**Step 1: Scaffold with Vite**

```bash
cd "C:/Users/King Hratch/intentguard"
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

**Step 2: Install dependencies**

```bash
cd "C:/Users/King Hratch/intentguard/frontend"
npm install tailwindcss @tailwindcss/vite recharts framer-motion @tanstack/react-query
```

**Step 3: Configure Tailwind with Vite plugin**

Update `frontend/vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
```

Replace `frontend/src/index.css` with:

```css
@import "tailwindcss";
```

**Step 4: Replace App.tsx with placeholder**

```tsx
function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <div className="flex items-center justify-center h-screen">
        <h1 className="text-4xl font-bold">IntentGuard</h1>
      </div>
    </div>
  );
}

export default App;
```

**Step 5: Create frontend/Dockerfile**

```dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host"]
```

**Step 6: Verify frontend starts**

```bash
cd "C:/Users/King Hratch/intentguard/frontend"
npm run dev &
# Expected: Local: http://localhost:5173/
# Visit in browser — should show dark page with "IntentGuard"
kill %1
```

**Step 7: Clean up Vite boilerplate**

Delete: `frontend/src/App.css`, `frontend/src/assets/react.svg`, `frontend/public/vite.svg`

**Step 8: Commit**

```bash
git add frontend/
git commit -m "feat: scaffold React + Vite + Tailwind frontend"
```

---

## Phase 2: Simulated Data & Database

### Task 4: Create SQLite Schema and Data Access Layer

**Files:**
- Create: `backend/app/data/database.py`
- Create: `backend/app/data/schema.sql`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/test_database.py`

**Step 1: Write the failing test**

```python
# backend/tests/test_database.py
import asyncio
import pytest
from app.data.database import get_db, init_db


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


def test_init_db_creates_tables(db_path):
    asyncio.run(_test_init(db_path))


async def _test_init(db_path):
    await init_db(db_path)
    async with get_db(db_path) as db:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in await cursor.fetchall()]
    assert "users" in tables
    assert "events" in tables
    assert "risk_scores" in tables
    assert "ux_clusters" in tables
```

**Step 2: Run test to verify it fails**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
source .venv/Scripts/activate
pip install pytest pytest-asyncio
python -m pytest tests/test_database.py -v
# Expected: FAIL — ModuleNotFoundError
```

**Step 3: Create schema.sql**

```sql
-- backend/app/data/schema.sql
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TEXT NOT NULL,
    account_type TEXT NOT NULL CHECK(account_type IN ('free', 'pro', 'enterprise')),
    scenario_tag TEXT NOT NULL CHECK(scenario_tag IN ('churn', 'fraud', 'normal', 'confused'))
);

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id),
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    properties TEXT NOT NULL DEFAULT '{}',
    CHECK(event_type IN (
        'page_view', 'api_call', 'login', 'payment', 'support_ticket',
        'search', 'feature_use', 'error', 'signup', 'message_sent'
    ))
);

CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);

CREATE TABLE IF NOT EXISTS risk_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL REFERENCES users(user_id),
    score_type TEXT NOT NULL CHECK(score_type IN ('churn', 'fraud', 'abuse')),
    score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
    top_features TEXT NOT NULL DEFAULT '[]',
    explanation TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_risk_user ON risk_scores(user_id);

CREATE TABLE IF NOT EXISTS ux_clusters (
    cluster_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    feature_area TEXT NOT NULL,
    message_count INTEGER NOT NULL,
    example_messages TEXT NOT NULL DEFAULT '[]',
    auto_summary TEXT NOT NULL,
    suggested_fix TEXT NOT NULL
);
```

**Step 4: Create database.py**

```python
# backend/app/data/database.py
import aiosqlite
from contextlib import asynccontextmanager
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


async def init_db(db_path: str) -> None:
    schema = SCHEMA_PATH.read_text()
    async with aiosqlite.connect(db_path) as db:
        await db.executescript(schema)
        await db.commit()


@asynccontextmanager
async def get_db(db_path: str):
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        yield db
```

**Step 5: Run test to verify it passes**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m pytest tests/test_database.py -v
# Expected: PASS
```

**Step 6: Commit**

```bash
git add backend/app/data/ backend/tests/
git commit -m "feat: add SQLite schema and database access layer"
```

---

### Task 5: Build Simulated Data Generators

**Files:**
- Create: `data/generators/__init__.py`
- Create: `data/generators/users.py`
- Create: `data/generators/events.py`
- Create: `data/generators/clusters.py`
- Create: `data/seed.py`
- Create: `data/tests/test_generators.py`

**Step 1: Write failing test for user generator**

```python
# data/tests/test_generators.py
from generators.users import generate_users


def test_generate_users_count():
    users = generate_users(count=10, seed=42)
    assert len(users) == 10


def test_generate_users_scenario_distribution():
    users = generate_users(count=50, seed=42)
    tags = [u["scenario_tag"] for u in users]
    assert "churn" in tags
    assert "fraud" in tags
    assert "normal" in tags
    assert "confused" in tags


def test_generate_users_fields():
    users = generate_users(count=1, seed=42)
    u = users[0]
    assert all(k in u for k in ["user_id", "name", "email", "created_at", "account_type", "scenario_tag"])
```

**Step 2: Run test to verify it fails**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python -m pytest tests/test_generators.py::test_generate_users_count -v
# Expected: FAIL — ModuleNotFoundError
```

**Step 3: Implement user generator**

```python
# data/generators/users.py
import random
import uuid
from datetime import datetime, timedelta

FIRST_NAMES = [
    "Alex", "Jordan", "Sam", "Morgan", "Taylor", "Casey", "Riley", "Quinn",
    "Avery", "Blake", "Cameron", "Dakota", "Emery", "Finley", "Harper", "Jamie",
    "Kai", "Logan", "Marley", "Nico", "Oakley", "Parker", "Reese", "Sage",
    "Tatum", "Val", "Wren", "Zion", "Drew", "Ellis", "Flynn", "Gray",
    "Hayden", "Indigo", "Jules", "Kit", "Lane", "Max", "Noel", "Onyx",
    "Phoenix", "Rain", "Sky", "Toni", "Uma", "Vesper", "Winter", "Xen",
    "Yael", "Zephyr",
]

LAST_NAMES = [
    "Chen", "Patel", "Kim", "Singh", "Nguyen", "Santos", "Rossi", "Muller",
    "Tanaka", "Ali", "Park", "Johansson", "Cohen", "Silva", "Garcia", "Okonkwo",
    "Dubois", "Ivanov", "Yamamoto", "Larsen", "Fernandez", "Bakshi", "Torres",
    "Schmidt", "Nakamura", "Bianchi", "Andersen", "Takahashi", "Chowdhury", "Petrov",
]

SCENARIO_WEIGHTS = {"churn": 0.25, "fraud": 0.15, "normal": 0.35, "confused": 0.25}
ACCOUNT_TYPES = ["free", "pro", "enterprise"]


def generate_users(count: int = 50, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    scenarios = list(SCENARIO_WEIGHTS.keys())
    weights = list(SCENARIO_WEIGHTS.values())
    base_date = datetime(2025, 6, 1)
    users = []

    for i in range(count):
        scenario = rng.choices(scenarios, weights=weights, k=1)[0]
        created = base_date + timedelta(days=rng.randint(0, 180))
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)

        users.append({
            "user_id": str(uuid.UUID(int=rng.getrandbits(128))),
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@example.com",
            "created_at": created.isoformat(),
            "account_type": rng.choice(ACCOUNT_TYPES),
            "scenario_tag": scenario,
        })

    return users
```

**Step 4: Run test to verify it passes**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python -m pytest tests/test_generators.py -v
# Expected: PASS
```

**Step 5: Implement event generator**

```python
# data/generators/events.py
import random
import uuid
import json
from datetime import datetime, timedelta

EVENT_TYPES = [
    "page_view", "api_call", "login", "payment", "support_ticket",
    "search", "feature_use", "error", "signup", "message_sent",
]

PAGES = ["/dashboard", "/settings", "/pricing", "/docs", "/billing", "/profile", "/features", "/integrations"]
FEATURES = ["export", "import", "webhook", "api-key", "team-invite", "sso", "analytics", "notifications"]
SEARCH_QUERIES_CONFUSED = [
    "how to export data", "export not working", "where is export button",
    "cant find export", "data export help", "download my data",
    "how to invite team", "team invite broken", "add team member",
    "where is team settings", "team management help",
]
SUPPORT_MESSAGES_CONFUSED = [
    "I can't find the export feature anywhere in the dashboard",
    "The export button seems to have disappeared after the update",
    "How do I download my data? I've looked everywhere",
    "Team invite link doesn't seem to work for my colleagues",
    "I'm trying to add a team member but the option is grayed out",
]


def generate_events_for_user(user: dict, seed: int = 42) -> list[dict]:
    rng = random.Random(seed + hash(user["user_id"]))
    created = datetime.fromisoformat(user["created_at"])
    scenario = user["scenario_tag"]
    events = []

    if scenario == "churn":
        events = _generate_churn_events(rng, user["user_id"], created)
    elif scenario == "fraud":
        events = _generate_fraud_events(rng, user["user_id"], created)
    elif scenario == "confused":
        events = _generate_confused_events(rng, user["user_id"], created)
    else:
        events = _generate_normal_events(rng, user["user_id"], created)

    return events


def _generate_churn_events(rng, user_id, created):
    events = []
    # Phase 1: Active (days 0-14)
    for day in range(15):
        ts = created + timedelta(days=day, hours=rng.randint(8, 20))
        for _ in range(rng.randint(3, 8)):
            ts += timedelta(minutes=rng.randint(1, 30))
            events.append(_event(rng, user_id, ts, "page_view", {"page": rng.choice(PAGES)}))
            if rng.random() < 0.3:
                events.append(_event(rng, user_id, ts, "feature_use", {"feature": rng.choice(FEATURES)}))

    # Phase 2: Friction (days 15-30) — pricing views, errors
    for day in range(15, 31):
        ts = created + timedelta(days=day, hours=rng.randint(8, 20))
        for _ in range(rng.randint(1, 4)):
            ts += timedelta(minutes=rng.randint(1, 30))
            if rng.random() < 0.4:
                events.append(_event(rng, user_id, ts, "page_view", {"page": "/pricing"}))
            if rng.random() < 0.3:
                events.append(_event(rng, user_id, ts, "error", {"code": rng.choice(["timeout", "403", "500"])}))
            events.append(_event(rng, user_id, ts, "page_view", {"page": rng.choice(PAGES)}))

    # Phase 3: Decline (days 31-60) — sparse logins
    for day in range(31, 61):
        if rng.random() < 0.2:
            ts = created + timedelta(days=day, hours=rng.randint(8, 20))
            events.append(_event(rng, user_id, ts, "login", {}))
            events.append(_event(rng, user_id, ts, "page_view", {"page": "/dashboard"}))

    return events


def _generate_fraud_events(rng, user_id, created):
    events = []
    # Rapid activity in first 3 days, unusual hours
    for day in range(3):
        for _ in range(rng.randint(15, 30)):
            hour = rng.choice([2, 3, 4, 23, 0, 1])  # unusual hours
            ts = created + timedelta(days=day, hours=hour, minutes=rng.randint(0, 59))
            event_type = rng.choices(
                ["api_call", "payment", "message_sent", "signup"],
                weights=[0.3, 0.3, 0.3, 0.1],
                k=1,
            )[0]
            props = {}
            if event_type == "payment":
                props = {"amount": round(rng.uniform(0.50, 4.99), 2), "currency": "USD"}
            elif event_type == "message_sent":
                props = {"template": True, "length": rng.randint(10, 20)}
            elif event_type == "api_call":
                props = {"endpoint": "/api/bulk", "count": rng.randint(50, 500)}
            events.append(_event(rng, user_id, ts, event_type, props))

    return events


def _generate_confused_events(rng, user_id, created):
    events = []
    for day in range(30):
        ts = created + timedelta(days=day, hours=rng.randint(9, 17))
        events.append(_event(rng, user_id, ts, "login", {}))

        # Regular usage
        for _ in range(rng.randint(2, 5)):
            ts += timedelta(minutes=rng.randint(1, 15))
            events.append(_event(rng, user_id, ts, "page_view", {"page": rng.choice(PAGES)}))

        # Confusion signals
        if rng.random() < 0.4:
            ts += timedelta(minutes=rng.randint(1, 5))
            events.append(_event(rng, user_id, ts, "search", {"query": rng.choice(SEARCH_QUERIES_CONFUSED)}))
        if rng.random() < 0.25:
            ts += timedelta(minutes=rng.randint(5, 30))
            events.append(_event(rng, user_id, ts, "support_ticket", {"message": rng.choice(SUPPORT_MESSAGES_CONFUSED)}))

    return events


def _generate_normal_events(rng, user_id, created):
    events = []
    for day in range(45):
        if rng.random() < 0.7:  # active ~70% of days
            ts = created + timedelta(days=day, hours=rng.randint(9, 17))
            events.append(_event(rng, user_id, ts, "login", {}))
            for _ in range(rng.randint(3, 10)):
                ts += timedelta(minutes=rng.randint(1, 20))
                event_type = rng.choices(
                    ["page_view", "feature_use", "api_call"],
                    weights=[0.5, 0.3, 0.2],
                    k=1,
                )[0]
                props = {}
                if event_type == "page_view":
                    props = {"page": rng.choice(PAGES)}
                elif event_type == "feature_use":
                    props = {"feature": rng.choice(FEATURES)}
                events.append(_event(rng, user_id, ts, event_type, props))
    return events


def _event(rng, user_id, ts, event_type, properties):
    return {
        "event_id": str(uuid.UUID(int=rng.getrandbits(128))),
        "user_id": user_id,
        "timestamp": ts.isoformat(),
        "event_type": event_type,
        "properties": json.dumps(properties),
    }
```

**Step 6: Implement cluster generator**

```python
# data/generators/clusters.py
import uuid

CLUSTERS = [
    {
        "label": "Export Feature Confusion",
        "feature_area": "data-export",
        "example_messages": [
            "I can't find the export feature anywhere in the dashboard",
            "The export button seems to have disappeared after the update",
            "How do I download my data? I've looked everywhere",
            "Export CSV option is missing from the reports page",
            "Where did the bulk export go? I used it last week",
        ],
        "auto_summary": "Users are struggling to locate the data export feature. 73% of confused users mention 'export' or 'download' in support tickets. The feature was moved during the v2.3 redesign but navigation hints were not updated.",
        "suggested_fix": "Add an 'Export' shortcut to the top-right toolbar and include a migration tooltip for users who last used the old export location.",
    },
    {
        "label": "Team Invite Flow Broken",
        "feature_area": "team-management",
        "example_messages": [
            "Team invite link doesn't seem to work for my colleagues",
            "I'm trying to add a team member but the option is grayed out",
            "How do I share access with my team? The invite button does nothing",
            "Sent 3 invites but nobody received them",
            "Team settings page shows 'upgrade required' but I'm already on Pro",
        ],
        "auto_summary": "Team invite flow has multiple friction points. Free-tier users see the invite button but get a confusing 'upgrade' message. Pro users report invite emails landing in spam. The grayed-out state lacks explanation.",
        "suggested_fix": "Hide invite button for free tier (show upgrade CTA instead). Add email delivery status tracking. Show clear tooltip explaining grayed-out states.",
    },
    {
        "label": "API Key Management Unclear",
        "feature_area": "developer-tools",
        "example_messages": [
            "Where do I find my API key?",
            "I regenerated my key and now nothing works",
            "The API docs say to use a bearer token but I only see an API key",
            "How many API keys can I have?",
            "Is there a way to create read-only API keys?",
        ],
        "auto_summary": "Developer users are confused about API key lifecycle and permissions. The docs reference 'bearer tokens' but the UI shows 'API keys'. Key regeneration has no warning about invalidating the old key.",
        "suggested_fix": "Unify terminology to 'API keys' everywhere. Add a confirmation dialog for key regeneration with impact warning. Add scoped key support (read-only, write, admin).",
    },
]


def generate_clusters() -> list[dict]:
    return [
        {
            "cluster_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, c["label"])),
            "label": c["label"],
            "feature_area": c["feature_area"],
            "message_count": len(c["example_messages"]) * 12,  # simulate more volume
            "example_messages": c["example_messages"],
            "auto_summary": c["auto_summary"],
            "suggested_fix": c["suggested_fix"],
        }
        for c in CLUSTERS
    ]
```

**Step 7: Write tests for events and clusters**

```python
# Append to data/tests/test_generators.py
from generators.events import generate_events_for_user
from generators.clusters import generate_clusters


def test_generate_events_churn_user():
    user = {
        "user_id": "test-churn-1",
        "created_at": "2025-06-01T00:00:00",
        "scenario_tag": "churn",
    }
    events = generate_events_for_user(user)
    assert len(events) > 20
    types = {e["event_type"] for e in events}
    assert "page_view" in types


def test_generate_events_fraud_user():
    user = {
        "user_id": "test-fraud-1",
        "created_at": "2025-06-01T00:00:00",
        "scenario_tag": "fraud",
    }
    events = generate_events_for_user(user)
    assert len(events) > 10
    types = {e["event_type"] for e in events}
    assert "payment" in types or "api_call" in types


def test_generate_clusters():
    clusters = generate_clusters()
    assert len(clusters) == 3
    assert all("cluster_id" in c for c in clusters)
    assert all("auto_summary" in c for c in clusters)
```

**Step 8: Run all generator tests**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python -m pytest tests/ -v
# Expected: all PASS
```

**Step 9: Commit**

```bash
git add data/
git commit -m "feat: add simulated data generators for users, events, and clusters"
```

---

### Task 6: Build Seed Script (Data Generation + DB Population)

**Files:**
- Create: `data/seed.py`
- Create: `data/tests/test_seed.py`

**Step 1: Write failing test**

```python
# data/tests/test_seed.py
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from seed import seed_database


def test_seed_populates_database(tmp_path):
    db_path = str(tmp_path / "test.db")
    asyncio.run(seed_database(db_path))

    import sqlite3
    conn = sqlite3.connect(db_path)
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    event_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    cluster_count = conn.execute("SELECT COUNT(*) FROM ux_clusters").fetchone()[0]
    conn.close()

    assert user_count == 50
    assert event_count > 1000
    assert cluster_count == 3
```

**Step 2: Run test to verify it fails**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python -m pytest tests/test_seed.py -v
# Expected: FAIL — ImportError
```

**Step 3: Implement seed.py**

```python
# data/seed.py
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import aiosqlite
from generators.users import generate_users
from generators.events import generate_events_for_user
from generators.clusters import generate_clusters

SCHEMA_PATH = Path(__file__).parent.parent / "backend" / "app" / "data" / "schema.sql"
DEFAULT_DB_PATH = str(Path(__file__).parent / "intentguard.db")


async def seed_database(db_path: str = DEFAULT_DB_PATH) -> None:
    schema = SCHEMA_PATH.read_text()

    async with aiosqlite.connect(db_path) as db:
        await db.executescript(schema)

        # Users
        users = generate_users(count=50, seed=42)
        await db.executemany(
            "INSERT INTO users (user_id, name, email, created_at, account_type, scenario_tag) VALUES (?, ?, ?, ?, ?, ?)",
            [(u["user_id"], u["name"], u["email"], u["created_at"], u["account_type"], u["scenario_tag"]) for u in users],
        )

        # Events
        all_events = []
        for user in users:
            all_events.extend(generate_events_for_user(user))
        await db.executemany(
            "INSERT INTO events (event_id, user_id, timestamp, event_type, properties) VALUES (?, ?, ?, ?, ?)",
            [(e["event_id"], e["user_id"], e["timestamp"], e["event_type"], e["properties"]) for e in all_events],
        )

        # Clusters
        clusters = generate_clusters()
        await db.executemany(
            "INSERT INTO ux_clusters (cluster_id, label, feature_area, message_count, example_messages, auto_summary, suggested_fix) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(c["cluster_id"], c["label"], c["feature_area"], c["message_count"], json.dumps(c["example_messages"]), c["auto_summary"], c["suggested_fix"]) for c in clusters],
        )

        await db.commit()

    print(f"Seeded {len(users)} users, {len(all_events)} events, {len(clusters)} clusters to {db_path}")


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB_PATH
    asyncio.run(seed_database(db_path))
```

**Step 4: Run test to verify it passes**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python -m pytest tests/test_seed.py -v
# Expected: PASS
```

**Step 5: Run seed for real**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python seed.py
# Expected: "Seeded 50 users, XXXX events, 3 clusters to .../intentguard.db"
```

**Step 6: Commit**

```bash
git add data/seed.py data/tests/test_seed.py
git commit -m "feat: add seed script to populate SQLite database"
```

---

## Phase 3: ML Pipeline

### Task 7: Feature Extraction

**Files:**
- Create: `backend/app/ml/features.py`
- Create: `backend/tests/test_features.py`

**Step 1: Write failing test**

```python
# backend/tests/test_features.py
from app.ml.features import extract_user_features


def test_extract_features_returns_dict():
    events = [
        {"timestamp": "2025-06-01T10:00:00", "event_type": "login", "properties": "{}"},
        {"timestamp": "2025-06-01T10:05:00", "event_type": "page_view", "properties": '{"page": "/pricing"}'},
        {"timestamp": "2025-06-01T10:10:00", "event_type": "error", "properties": '{"code": "500"}'},
    ]
    features = extract_user_features(events)
    assert isinstance(features, dict)
    assert "total_events" in features
    assert "error_rate" in features
    assert "pricing_page_views" in features
    assert features["total_events"] == 3
    assert features["error_rate"] > 0
    assert features["pricing_page_views"] == 1
```

**Step 2: Run test to verify it fails**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m pytest tests/test_features.py -v
# Expected: FAIL
```

**Step 3: Implement feature extraction**

```python
# backend/app/ml/features.py
import json
from datetime import datetime
from collections import Counter


def extract_user_features(events: list[dict]) -> dict:
    if not events:
        return _empty_features()

    timestamps = [datetime.fromisoformat(e["timestamp"]) for e in events]
    types = [e["event_type"] for e in events]
    type_counts = Counter(types)

    total = len(events)
    span_days = max((max(timestamps) - min(timestamps)).days, 1)

    # Parse properties
    props = []
    for e in events:
        p = e.get("properties", "{}")
        props.append(json.loads(p) if isinstance(p, str) else p)

    # Page-specific counts
    page_views = [p.get("page", "") for e, p in zip(events, props) if e["event_type"] == "page_view"]
    pricing_views = sum(1 for p in page_views if p == "/pricing")

    # Time-based features
    hours = [t.hour for t in timestamps]
    unusual_hour_ratio = sum(1 for h in hours if h < 6 or h > 22) / max(len(hours), 1)

    # Payment features
    payments = [p for e, p in zip(events, props) if e["event_type"] == "payment"]
    payment_count = len(payments)
    avg_payment = sum(p.get("amount", 0) for p in payments) / max(payment_count, 1)
    small_payment_ratio = sum(1 for p in payments if p.get("amount", 0) < 5) / max(payment_count, 1)

    # Support/search features
    support_count = type_counts.get("support_ticket", 0)
    search_count = type_counts.get("search", 0)

    # Activity trend: compare first half vs second half event counts
    mid = timestamps[0] + (timestamps[-1] - timestamps[0]) / 2
    first_half = sum(1 for t in timestamps if t <= mid)
    second_half = total - first_half
    activity_trend = (second_half - first_half) / max(total, 1)  # negative = declining

    # Template message ratio (fraud signal)
    messages = [p for e, p in zip(events, props) if e["event_type"] == "message_sent"]
    template_ratio = sum(1 for m in messages if m.get("template")) / max(len(messages), 1)

    # API bulk calls (fraud signal)
    api_calls = [p for e, p in zip(events, props) if e["event_type"] == "api_call"]
    bulk_api_ratio = sum(1 for a in api_calls if a.get("count", 0) > 100) / max(len(api_calls), 1)

    return {
        "total_events": total,
        "span_days": span_days,
        "events_per_day": total / span_days,
        "login_count": type_counts.get("login", 0),
        "error_count": type_counts.get("error", 0),
        "error_rate": type_counts.get("error", 0) / total,
        "page_view_count": type_counts.get("page_view", 0),
        "pricing_page_views": pricing_views,
        "feature_use_count": type_counts.get("feature_use", 0),
        "payment_count": payment_count,
        "avg_payment_amount": avg_payment,
        "small_payment_ratio": small_payment_ratio,
        "support_ticket_count": support_count,
        "search_count": search_count,
        "unusual_hour_ratio": unusual_hour_ratio,
        "activity_trend": activity_trend,
        "template_message_ratio": template_ratio,
        "bulk_api_ratio": bulk_api_ratio,
        "unique_event_types": len(type_counts),
    }


def _empty_features():
    return {k: 0 for k in [
        "total_events", "span_days", "events_per_day", "login_count",
        "error_count", "error_rate", "page_view_count", "pricing_page_views",
        "feature_use_count", "payment_count", "avg_payment_amount",
        "small_payment_ratio", "support_ticket_count", "search_count",
        "unusual_hour_ratio", "activity_trend", "template_message_ratio",
        "bulk_api_ratio", "unique_event_types",
    ]}


FEATURE_NAMES = list(_empty_features().keys())
```

**Step 4: Run test to verify it passes**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m pytest tests/test_features.py -v
# Expected: PASS
```

**Step 5: Commit**

```bash
git add backend/app/ml/features.py backend/tests/test_features.py
git commit -m "feat: add feature extraction from user event streams"
```

---

### Task 8: ML Model Training and Scoring

**Files:**
- Create: `backend/app/ml/scoring.py`
- Create: `backend/app/ml/explain.py`
- Create: `backend/tests/test_scoring.py`

**Step 1: Write failing test**

```python
# backend/tests/test_scoring.py
from app.ml.scoring import ChurnModel, FraudModel
from app.ml.features import extract_user_features


def _make_churn_events():
    """Simulate a churning user's events."""
    events = []
    for i in range(20):
        events.append({"timestamp": f"2025-06-{1+i:02d}T10:00:00", "event_type": "page_view", "properties": '{"page": "/pricing"}'})
    for i in range(5):
        events.append({"timestamp": f"2025-06-{22+i:02d}T10:00:00", "event_type": "error", "properties": '{"code": "500"}'})
    return events


def _make_normal_events():
    events = []
    for i in range(30):
        events.append({"timestamp": f"2025-06-{1+(i%28):02d}T10:00:00", "event_type": "login", "properties": "{}"})
        events.append({"timestamp": f"2025-06-{1+(i%28):02d}T10:05:00", "event_type": "feature_use", "properties": '{"feature": "export"}'})
    return events


def test_churn_model_predict():
    model = ChurnModel()
    # Train with minimal data
    training_data = [
        (extract_user_features(_make_churn_events()), 1),
        (extract_user_features(_make_normal_events()), 0),
    ] * 10  # duplicate to meet min samples
    features_list = [f for f, _ in training_data]
    labels = [l for _, l in training_data]
    model.train(features_list, labels)

    score = model.predict(extract_user_features(_make_churn_events()))
    assert 0 <= score["score"] <= 100
    assert len(score["top_features"]) > 0
    assert isinstance(score["explanation"], str)


def test_fraud_model_predict():
    model = FraudModel()
    features = [extract_user_features(_make_normal_events())] * 20
    model.train(features)

    anomaly_features = extract_user_features(_make_churn_events())  # different pattern
    score = model.predict(anomaly_features)
    assert 0 <= score["score"] <= 100
```

**Step 2: Run test to verify it fails**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m pytest tests/test_scoring.py -v
# Expected: FAIL — ImportError
```

**Step 3: Implement explain.py**

```python
# backend/app/ml/explain.py

FEATURE_TEMPLATES = {
    "pricing_page_views": "Visited the pricing page {value:.0f} times",
    "error_rate": "Encountered errors in {value:.0%} of interactions",
    "error_count": "Hit {value:.0f} errors total",
    "activity_trend": "Activity is {'declining' if value < 0 else 'increasing'} ({value:+.0%})",
    "login_count": "Logged in {value:.0f} times",
    "unusual_hour_ratio": "{value:.0%} of activity during unusual hours (late night/early morning)",
    "payment_count": "Made {value:.0f} payments",
    "small_payment_ratio": "{value:.0%} of payments were under $5",
    "template_message_ratio": "{value:.0%} of messages used templates",
    "bulk_api_ratio": "{value:.0%} of API calls were bulk operations",
    "support_ticket_count": "Filed {value:.0f} support tickets",
    "search_count": "Searched {value:.0f} times",
    "events_per_day": "Average {value:.1f} events per day",
    "span_days": "Active over {value:.0f} days",
    "feature_use_count": "Used {value:.0f} features",
}

ACTION_THRESHOLDS = {
    "churn": [
        (80, "Urgent: Schedule a personal check-in call within 24 hours"),
        (60, "Send targeted re-engagement email with feature highlights"),
        (40, "Add to watch list for weekly review"),
        (0, "No action needed — healthy engagement"),
    ],
    "fraud": [
        (80, "Block account and escalate to Trust & Safety for review"),
        (60, "Rate-limit API access and require identity verification"),
        (40, "Flag for manual review within 48 hours"),
        (0, "No action needed — normal patterns"),
    ],
}


def explain_features(top_features: list[tuple[str, float]]) -> str:
    parts = []
    for name, value in top_features[:5]:
        template = FEATURE_TEMPLATES.get(name)
        if template:
            try:
                text = eval(f'f"""{template}"""')
            except Exception:
                text = f"{name.replace('_', ' ').title()}: {value:.2f}"
        else:
            text = f"{name.replace('_', ' ').title()}: {value:.2f}"
        parts.append(f"- {text}")
    return "\n".join(parts)


def recommend_action(score_type: str, score: float) -> str:
    thresholds = ACTION_THRESHOLDS.get(score_type, ACTION_THRESHOLDS["churn"])
    for threshold, action in thresholds:
        if score >= threshold:
            return action
    return "Monitor"
```

**Step 4: Implement scoring.py**

```python
# backend/app/ml/scoring.py
import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, IsolationForest

from app.ml.features import FEATURE_NAMES
from app.ml.explain import explain_features, recommend_action


class ChurnModel:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=50, max_depth=3, random_state=42
        )
        self.trained = False

    def train(self, features_list: list[dict], labels: list[int]) -> None:
        X = np.array([[f.get(k, 0) for k in FEATURE_NAMES] for f in features_list])
        y = np.array(labels)
        self.model.fit(X, y)
        self.trained = True

    def predict(self, features: dict) -> dict:
        X = np.array([[features.get(k, 0) for k in FEATURE_NAMES]])
        proba = self.model.predict_proba(X)[0][1]  # probability of churn
        score = round(proba * 100, 1)

        importances = self.model.feature_importances_
        feature_values = [(FEATURE_NAMES[i], features.get(FEATURE_NAMES[i], 0))
                          for i in np.argsort(importances)[::-1][:5]]

        return {
            "score": score,
            "confidence": round(max(proba, 1 - proba), 3),
            "top_features": feature_values,
            "explanation": explain_features(feature_values),
            "recommended_action": recommend_action("churn", score),
        }

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.trained = True


class FraudModel:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=50, contamination=0.15, random_state=42
        )
        self.trained = False

    def train(self, features_list: list[dict]) -> None:
        X = np.array([[f.get(k, 0) for k in FEATURE_NAMES] for f in features_list])
        self.model.fit(X)
        self.trained = True

    def predict(self, features: dict) -> dict:
        X = np.array([[features.get(k, 0) for k in FEATURE_NAMES]])
        raw_score = -self.model.score_samples(X)[0]  # higher = more anomalous
        score = round(min(max(raw_score * 50, 0), 100), 1)  # normalize to 0-100

        # Use feature deviations as importance proxy
        feature_vals = [(FEATURE_NAMES[i], features.get(FEATURE_NAMES[i], 0))
                        for i in range(len(FEATURE_NAMES))]
        feature_vals.sort(key=lambda x: abs(x[1]), reverse=True)
        top_features = feature_vals[:5]

        return {
            "score": score,
            "confidence": round(min(raw_score / 2, 1.0), 3),
            "top_features": top_features,
            "explanation": explain_features(top_features),
            "recommended_action": recommend_action("fraud", score),
        }

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.trained = True
```

**Step 5: Run tests to verify they pass**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m pytest tests/test_scoring.py -v
# Expected: PASS
```

**Step 6: Commit**

```bash
git add backend/app/ml/ backend/tests/test_scoring.py
git commit -m "feat: add churn and fraud ML models with explanation generation"
```

---

### Task 9: Model Training Script (integrated with seed)

**Files:**
- Create: `data/train_models.py`

**Step 1: Implement train_models.py**

```python
# data/train_models.py
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import aiosqlite
from app.ml.features import extract_user_features
from app.ml.scoring import ChurnModel, FraudModel

DEFAULT_DB = str(Path(__file__).parent / "intentguard.db")
MODELS_DIR = Path(__file__).parent.parent / "models"


async def train_and_save(db_path: str = DEFAULT_DB):
    MODELS_DIR.mkdir(exist_ok=True)

    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

        # Load all users
        cursor = await db.execute("SELECT user_id, scenario_tag FROM users")
        users = await cursor.fetchall()

        features_list = []
        churn_labels = []

        for user in users:
            uid = user["user_id"]
            tag = user["scenario_tag"]

            ecursor = await db.execute(
                "SELECT timestamp, event_type, properties FROM events WHERE user_id = ? ORDER BY timestamp",
                (uid,),
            )
            events = [dict(row) for row in await ecursor.fetchall()]

            if not events:
                continue

            features = extract_user_features(events)
            features_list.append(features)
            churn_labels.append(1 if tag == "churn" else 0)

        # Train churn model
        churn_model = ChurnModel()
        churn_model.train(features_list, churn_labels)
        churn_model.save(str(MODELS_DIR / "churn_model.pkl"))
        print(f"Churn model saved ({sum(churn_labels)}/{len(churn_labels)} positive)")

        # Train fraud model (unsupervised — trained on all data)
        fraud_model = FraudModel()
        fraud_model.train(features_list)
        fraud_model.save(str(MODELS_DIR / "fraud_model.pkl"))
        print(f"Fraud model saved (trained on {len(features_list)} users)")

        # Compute and store risk scores for all users
        cursor = await db.execute("SELECT user_id, scenario_tag FROM users")
        users = await cursor.fetchall()

        for user in users:
            uid = user["user_id"]
            ecursor = await db.execute(
                "SELECT timestamp, event_type, properties FROM events WHERE user_id = ? ORDER BY timestamp",
                (uid,),
            )
            events = [dict(row) for row in await ecursor.fetchall()]
            if not events:
                continue

            features = extract_user_features(events)

            churn_result = churn_model.predict(features)
            fraud_result = fraud_model.predict(features)

            for score_type, result in [("churn", churn_result), ("fraud", fraud_result)]:
                await db.execute(
                    """INSERT INTO risk_scores
                       (user_id, score_type, score, confidence, top_features, explanation, recommended_action, computed_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
                    (uid, score_type, result["score"], result["confidence"],
                     json.dumps(result["top_features"]), result["explanation"],
                     result["recommended_action"]),
                )

        await db.commit()
        print("Risk scores computed and stored for all users")


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB
    asyncio.run(train_and_save(db_path))
```

**Step 2: Run it**

```bash
cd "C:/Users/King Hratch/intentguard/data"
python seed.py && python train_models.py
# Expected: Models saved, scores computed
```

**Step 3: Commit**

```bash
git add data/train_models.py
git commit -m "feat: add model training script with risk score precomputation"
```

---

## Phase 4: Backend API Routes

### Task 10: Pydantic Models

**Files:**
- Create: `backend/app/models/schemas.py`

**Step 1: Create schemas**

```python
# backend/app/models/schemas.py
from pydantic import BaseModel


class UserSummary(BaseModel):
    user_id: str
    name: str
    email: str
    created_at: str
    account_type: str
    scenario_tag: str
    churn_score: float | None = None
    fraud_score: float | None = None


class Event(BaseModel):
    event_id: str
    user_id: str
    timestamp: str
    event_type: str
    properties: dict


class RiskScore(BaseModel):
    score_type: str
    score: float
    confidence: float
    top_features: list
    explanation: str
    recommended_action: str
    computed_at: str


class UserDetail(BaseModel):
    user_id: str
    name: str
    email: str
    created_at: str
    account_type: str
    scenario_tag: str
    risk_scores: list[RiskScore]


class UxCluster(BaseModel):
    cluster_id: str
    label: str
    feature_area: str
    message_count: int
    example_messages: list[str]
    auto_summary: str
    suggested_fix: str


class OverviewStats(BaseModel):
    total_users: int
    total_events: int
    high_risk_churn: int
    high_risk_fraud: int
    cluster_count: int


class TimelineResponse(BaseModel):
    events: list[Event]
    total: int


class RiskTrend(BaseModel):
    score_type: str
    scores: list[RiskScore]
```

**Step 2: Commit**

```bash
git add backend/app/models/schemas.py
git commit -m "feat: add Pydantic response schemas"
```

---

### Task 11: API Route Handlers

**Files:**
- Create: `backend/app/api/users.py`
- Create: `backend/app/api/insights.py`
- Create: `backend/app/api/stats.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_api.py`

**Step 1: Write failing test**

```python
# backend/tests/test_api.py
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.anyio
async def test_list_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/users")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "user_id" in data[0]


@pytest.mark.anyio
async def test_overview_stats():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/stats/overview")
    assert r.status_code == 200
    data = r.json()
    assert "total_users" in data
```

**Step 2: Run test to verify it fails**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
pip install httpx anyio pytest-anyio
python -m pytest tests/test_api.py -v
# Expected: FAIL — route not found or 404
```

**Step 3: Add DB dependency to main.py**

```python
# backend/app/main.py
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.users import router as users_router
from app.api.insights import router as insights_router
from app.api.stats import router as stats_router

DB_PATH = str(Path(__file__).parent.parent.parent / "data" / "intentguard.db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_path = DB_PATH
    yield


app = FastAPI(
    title="IntentGuard API",
    description="Explainable user-behavior & risk intelligence",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
app.include_router(stats_router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

**Step 4: Implement users router**

```python
# backend/app/api/users.py
import json
from fastapi import APIRouter, Request, Query
import aiosqlite

router = APIRouter()


@router.get("/users")
async def list_users(
    request: Request,
    scenario: str | None = Query(None),
    risk_level: str | None = Query(None),
):
    db_path = request.app.state.db_path
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

        query = """
            SELECT u.*,
                   (SELECT score FROM risk_scores WHERE user_id = u.user_id AND score_type = 'churn' ORDER BY computed_at DESC LIMIT 1) as churn_score,
                   (SELECT score FROM risk_scores WHERE user_id = u.user_id AND score_type = 'fraud' ORDER BY computed_at DESC LIMIT 1) as fraud_score
            FROM users u
            WHERE 1=1
        """
        params = []
        if scenario:
            query += " AND u.scenario_tag = ?"
            params.append(scenario)

        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()

        users = [dict(row) for row in rows]

        if risk_level == "high":
            users = [u for u in users if (u.get("churn_score") or 0) >= 60 or (u.get("fraud_score") or 0) >= 60]
        elif risk_level == "low":
            users = [u for u in users if (u.get("churn_score") or 0) < 40 and (u.get("fraud_score") or 0) < 40]

    return users


@router.get("/users/{user_id}")
async def get_user(request: Request, user_id: str):
    db_path = request.app.state.db_path
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()
        if not user:
            return {"error": "User not found"}, 404

        cursor = await db.execute(
            "SELECT * FROM risk_scores WHERE user_id = ? ORDER BY computed_at DESC", (user_id,)
        )
        scores = await cursor.fetchall()

        result = dict(user)
        result["risk_scores"] = [
            {**dict(s), "top_features": json.loads(s["top_features"])}
            for s in scores
        ]

    return result


@router.get("/users/{user_id}/timeline")
async def get_timeline(
    request: Request,
    user_id: str,
    event_type: str | None = Query(None),
    limit: int = Query(100),
    offset: int = Query(0),
):
    db_path = request.app.state.db_path
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

        count_query = "SELECT COUNT(*) as total FROM events WHERE user_id = ?"
        data_query = "SELECT * FROM events WHERE user_id = ?"
        params = [user_id]

        if event_type:
            count_query += " AND event_type = ?"
            data_query += " AND event_type = ?"
            params.append(event_type)

        count_cursor = await db.execute(count_query, params)
        total = (await count_cursor.fetchone())["total"]

        data_query += " ORDER BY timestamp ASC LIMIT ? OFFSET ?"
        cursor = await db.execute(data_query, params + [limit, offset])
        events = [
            {**dict(row), "properties": json.loads(row["properties"])}
            for row in await cursor.fetchall()
        ]

    return {"events": events, "total": total}


@router.get("/users/{user_id}/risk")
async def get_risk(request: Request, user_id: str):
    db_path = request.app.state.db_path
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM risk_scores WHERE user_id = ? ORDER BY computed_at DESC",
            (user_id,),
        )
        scores = [
            {**dict(s), "top_features": json.loads(s["top_features"])}
            for s in await cursor.fetchall()
        ]
    return scores


@router.post("/users/{user_id}/risk/recalculate")
async def recalculate_risk(request: Request, user_id: str):
    db_path = request.app.state.db_path
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT timestamp, event_type, properties FROM events WHERE user_id = ? ORDER BY timestamp",
            (user_id,),
        )
        events = [dict(row) for row in await cursor.fetchall()]

    if not events:
        return {"error": "No events found"}

    from app.ml.features import extract_user_features
    from app.ml.scoring import ChurnModel, FraudModel
    from pathlib import Path

    models_dir = Path(__file__).parent.parent.parent.parent / "models"
    features = extract_user_features(events)

    results = []
    for ModelClass, name, path in [
        (ChurnModel, "churn", models_dir / "churn_model.pkl"),
        (FraudModel, "fraud", models_dir / "fraud_model.pkl"),
    ]:
        model = ModelClass()
        model.load(str(path))
        result = model.predict(features)
        results.append({"score_type": name, **result})

    return results
```

**Step 5: Implement insights router**

```python
# backend/app/api/insights.py
import json
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/insights/clusters")
async def list_clusters(request: Request):
    db_path = request.app.state.db_path
    import aiosqlite
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM ux_clusters")
        clusters = [
            {**dict(row), "example_messages": json.loads(row["example_messages"])}
            for row in await cursor.fetchall()
        ]
    return clusters


@router.get("/insights/clusters/{cluster_id}")
async def get_cluster(request: Request, cluster_id: str):
    db_path = request.app.state.db_path
    import aiosqlite
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM ux_clusters WHERE cluster_id = ?", (cluster_id,))
        row = await cursor.fetchone()
        if not row:
            return {"error": "Cluster not found"}, 404
        cluster = {**dict(row), "example_messages": json.loads(row["example_messages"])}
    return cluster
```

**Step 6: Implement stats router**

```python
# backend/app/api/stats.py
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/stats/overview")
async def overview(request: Request):
    db_path = request.app.state.db_path
    import aiosqlite
    async with aiosqlite.connect(db_path) as db:
        total_users = (await (await db.execute("SELECT COUNT(*) FROM users")).fetchone())[0]
        total_events = (await (await db.execute("SELECT COUNT(*) FROM events")).fetchone())[0]
        high_churn = (await (await db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM risk_scores WHERE score_type='churn' AND score >= 60"
        )).fetchone())[0]
        high_fraud = (await (await db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM risk_scores WHERE score_type='fraud' AND score >= 60"
        )).fetchone())[0]
        clusters = (await (await db.execute("SELECT COUNT(*) FROM ux_clusters")).fetchone())[0]

    return {
        "total_users": total_users,
        "total_events": total_events,
        "high_risk_churn": high_churn,
        "high_risk_fraud": high_fraud,
        "cluster_count": clusters,
    }
```

**Step 7: Run tests**

```bash
cd "C:/Users/King Hratch/intentguard/backend"
python -m pytest tests/test_api.py -v
# Expected: PASS (requires seeded DB)
```

**Step 8: Commit**

```bash
git add backend/app/api/ backend/app/main.py backend/app/models/schemas.py backend/tests/test_api.py
git commit -m "feat: add all API routes (users, insights, stats)"
```

---

## Phase 5: Frontend — Core Components

### Task 12: API Client and Query Provider

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/types.ts`
- Modify: `frontend/src/main.tsx`

**Step 1: Create types**

```typescript
// frontend/src/api/types.ts
export interface UserSummary {
  user_id: string;
  name: string;
  email: string;
  created_at: string;
  account_type: string;
  scenario_tag: string;
  churn_score: number | null;
  fraud_score: number | null;
}

export interface Event {
  event_id: string;
  user_id: string;
  timestamp: string;
  event_type: string;
  properties: Record<string, unknown>;
}

export interface RiskScore {
  score_type: string;
  score: number;
  confidence: number;
  top_features: [string, number][];
  explanation: string;
  recommended_action: string;
  computed_at: string;
}

export interface UserDetail extends UserSummary {
  risk_scores: RiskScore[];
}

export interface UxCluster {
  cluster_id: string;
  label: string;
  feature_area: string;
  message_count: number;
  example_messages: string[];
  auto_summary: string;
  suggested_fix: string;
}

export interface OverviewStats {
  total_users: number;
  total_events: number;
  high_risk_churn: number;
  high_risk_fraud: number;
  cluster_count: number;
}

export interface TimelineResponse {
  events: Event[];
  total: number;
}
```

**Step 2: Create API client**

```typescript
// frontend/src/api/client.ts
import type {
  UserSummary, UserDetail, TimelineResponse,
  RiskScore, UxCluster, OverviewStats,
} from "./types";

const BASE = "/api";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  getUsers: (params?: { scenario?: string; risk_level?: string }) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<UserSummary[]>(`/users${qs ? `?${qs}` : ""}`);
  },
  getUser: (id: string) => fetchJson<UserDetail>(`/users/${id}`),
  getTimeline: (id: string, params?: { event_type?: string; limit?: number; offset?: number }) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params || {}).map(([k, v]) => [k, String(v)]))
    ).toString();
    return fetchJson<TimelineResponse>(`/users/${id}/timeline${qs ? `?${qs}` : ""}`);
  },
  getRisk: (id: string) => fetchJson<RiskScore[]>(`/users/${id}/risk`),
  recalculateRisk: (id: string) =>
    fetchJson<RiskScore[]>(`/users/${id}/risk/recalculate`),
  getClusters: () => fetchJson<UxCluster[]>("/insights/clusters"),
  getCluster: (id: string) => fetchJson<UxCluster>(`/insights/clusters/${id}`),
  getStats: () => fetchJson<OverviewStats>("/stats/overview"),
};
```

**Step 3: Wrap App with QueryClientProvider in main.tsx**

```typescript
// frontend/src/main.tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./index.css";

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000 } },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>
);
```

**Step 4: Commit**

```bash
git add frontend/src/api/ frontend/src/main.tsx
git commit -m "feat: add API client, TypeScript types, and query provider"
```

---

### Task 13: RiskGauge Component

**Files:**
- Create: `frontend/src/components/RiskGauge.tsx`

**Step 1: Implement**

```tsx
// frontend/src/components/RiskGauge.tsx
interface RiskGaugeProps {
  label: string;
  score: number;
  size?: number;
}

export function RiskGauge({ label, score, size = 120 }: RiskGaugeProps) {
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;

  const color =
    score >= 70 ? "#ef4444" : score >= 40 ? "#f59e0b" : "#22c55e";

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#1f2937"
          strokeWidth={8}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={8}
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          strokeLinecap="round"
          className="transition-all duration-700"
        />
        <text
          x={size / 2}
          y={size / 2}
          textAnchor="middle"
          dominantBaseline="central"
          className="rotate-90 origin-center fill-gray-100 text-xl font-bold"
          style={{ fontSize: size * 0.22 }}
        >
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
        {label}
      </span>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add frontend/src/components/RiskGauge.tsx
git commit -m "feat: add RiskGauge circular score component"
```

---

### Task 14: TimelineView Component

**Files:**
- Create: `frontend/src/components/TimelineView.tsx`

**Step 1: Implement**

```tsx
// frontend/src/components/TimelineView.tsx
import type { Event } from "../api/types";

const EVENT_COLORS: Record<string, string> = {
  page_view: "#60a5fa",
  api_call: "#a78bfa",
  login: "#34d399",
  payment: "#fbbf24",
  support_ticket: "#f87171",
  search: "#38bdf8",
  feature_use: "#818cf8",
  error: "#ef4444",
  signup: "#4ade80",
  message_sent: "#fb923c",
};

interface TimelineViewProps {
  events: Event[];
}

export function TimelineView({ events }: TimelineViewProps) {
  return (
    <div className="overflow-x-auto">
      <div className="flex items-start gap-1 min-w-max py-4 px-2">
        {events.map((event) => (
          <div
            key={event.event_id}
            className="group relative flex flex-col items-center"
          >
            <div
              className="w-3 h-3 rounded-full cursor-pointer hover:scale-150 transition-transform"
              style={{ backgroundColor: EVENT_COLORS[event.event_type] || "#6b7280" }}
            />
            <div className="absolute bottom-full mb-2 hidden group-hover:block z-10">
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-xs shadow-xl min-w-48">
                <div className="font-semibold text-gray-100">{event.event_type}</div>
                <div className="text-gray-400 mt-1">
                  {new Date(event.timestamp).toLocaleString()}
                </div>
                {Object.keys(event.properties).length > 0 && (
                  <pre className="text-gray-500 mt-1 text-[10px]">
                    {JSON.stringify(event.properties, null, 2)}
                  </pre>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-3 flex-wrap px-2 mt-2">
        {Object.entries(EVENT_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-1 text-[10px] text-gray-500">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
            {type}
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add frontend/src/components/TimelineView.tsx
git commit -m "feat: add TimelineView event stream component"
```

---

### Task 15: ExplanationPanel and ActionCard Components

**Files:**
- Create: `frontend/src/components/ExplanationPanel.tsx`
- Create: `frontend/src/components/ActionCard.tsx`

**Step 1: Implement ExplanationPanel**

```tsx
// frontend/src/components/ExplanationPanel.tsx
import type { RiskScore } from "../api/types";

interface ExplanationPanelProps {
  risk: RiskScore;
}

export function ExplanationPanel({ risk }: ExplanationPanelProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wider">
          Why this score?
        </h3>
        <span className="text-xs text-gray-500">
          Confidence: {(risk.confidence * 100).toFixed(0)}%
        </span>
      </div>
      <div className="space-y-2">
        {risk.top_features.map(([feature, value], i) => (
          <div key={feature} className="flex items-center gap-3">
            <span className="text-xs text-gray-500 w-4">{i + 1}.</span>
            <div className="flex-1">
              <div className="text-sm text-gray-300">
                {feature.replace(/_/g, " ")}
              </div>
              <div className="h-1.5 bg-gray-800 rounded-full mt-1">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(Math.abs(Number(value)) * 10, 100)}%` }}
                />
              </div>
            </div>
            <span className="text-xs font-mono text-gray-400">
              {typeof value === "number" ? value.toFixed(2) : value}
            </span>
          </div>
        ))}
      </div>
      <pre className="mt-4 text-xs text-gray-500 whitespace-pre-wrap">
        {risk.explanation}
      </pre>
    </div>
  );
}
```

**Step 2: Implement ActionCard**

```tsx
// frontend/src/components/ActionCard.tsx
interface ActionCardProps {
  action: string;
  score: number;
}

const SEVERITY_CONFIG = [
  { min: 80, label: "CRITICAL", bg: "bg-red-950", border: "border-red-700", text: "text-red-400" },
  { min: 60, label: "HIGH", bg: "bg-orange-950", border: "border-orange-700", text: "text-orange-400" },
  { min: 40, label: "MEDIUM", bg: "bg-yellow-950", border: "border-yellow-700", text: "text-yellow-400" },
  { min: 0, label: "LOW", bg: "bg-green-950", border: "border-green-700", text: "text-green-400" },
];

export function ActionCard({ action, score }: ActionCardProps) {
  const severity = SEVERITY_CONFIG.find((s) => score >= s.min)!;

  return (
    <div className={`${severity.bg} border ${severity.border} rounded-lg p-4`}>
      <div className="flex items-center gap-2 mb-2">
        <span className={`text-xs font-bold ${severity.text} uppercase`}>
          {severity.label}
        </span>
        <span className="text-xs text-gray-500">Recommended Action</span>
      </div>
      <p className="text-sm text-gray-200">{action}</p>
    </div>
  );
}
```

**Step 3: Commit**

```bash
git add frontend/src/components/ExplanationPanel.tsx frontend/src/components/ActionCard.tsx
git commit -m "feat: add ExplanationPanel and ActionCard components"
```

---

### Task 16: FeatureImportanceChart Component

**Files:**
- Create: `frontend/src/components/FeatureImportanceChart.tsx`

**Step 1: Implement**

```tsx
// frontend/src/components/FeatureImportanceChart.tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface FeatureImportanceChartProps {
  features: [string, number][];
}

export function FeatureImportanceChart({ features }: FeatureImportanceChartProps) {
  const data = features.map(([name, value]) => ({
    name: name.replace(/_/g, " "),
    value: Math.abs(Number(value)),
    raw: Number(value),
  }));

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wider mb-3">
        Top Contributing Factors
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical" margin={{ left: 100 }}>
          <XAxis type="number" stroke="#4b5563" tick={{ fill: "#9ca3af", fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="name"
            stroke="#4b5563"
            tick={{ fill: "#d1d5db", fontSize: 11 }}
            width={100}
          />
          <Tooltip
            contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
            labelStyle={{ color: "#f3f4f6" }}
            itemStyle={{ color: "#93c5fd" }}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={i === 0 ? "#3b82f6" : i === 1 ? "#60a5fa" : "#93c5fd"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add frontend/src/components/FeatureImportanceChart.tsx
git commit -m "feat: add FeatureImportanceChart horizontal bar chart"
```

---

### Task 17: ClusterView Component

**Files:**
- Create: `frontend/src/components/ClusterView.tsx`

**Step 1: Implement**

```tsx
// frontend/src/components/ClusterView.tsx
import { useState } from "react";
import type { UxCluster } from "../api/types";

interface ClusterViewProps {
  clusters: UxCluster[];
}

export function ClusterView({ clusters }: ClusterViewProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {clusters.map((cluster) => (
        <div
          key={cluster.cluster_id}
          className="bg-gray-900 border border-gray-800 rounded-lg p-4 cursor-pointer hover:border-gray-600 transition-colors"
          onClick={() =>
            setExpanded(expanded === cluster.cluster_id ? null : cluster.cluster_id)
          }
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono text-blue-400 bg-blue-950 px-2 py-0.5 rounded">
              {cluster.feature_area}
            </span>
            <span className="text-xs text-gray-500">{cluster.message_count} reports</span>
          </div>
          <h4 className="font-semibold text-gray-100 mb-2">{cluster.label}</h4>
          <p className="text-sm text-gray-400 mb-3">{cluster.auto_summary}</p>

          {expanded === cluster.cluster_id && (
            <div className="mt-3 pt-3 border-t border-gray-800">
              <h5 className="text-xs font-semibold text-gray-300 uppercase mb-2">
                Example Messages
              </h5>
              <ul className="space-y-1.5">
                {cluster.example_messages.map((msg, i) => (
                  <li key={i} className="text-xs text-gray-500 pl-3 border-l-2 border-gray-700">
                    {msg}
                  </li>
                ))}
              </ul>
              <div className="mt-3 p-2 bg-green-950 border border-green-800 rounded text-xs text-green-300">
                <span className="font-semibold">Suggested Fix: </span>
                {cluster.suggested_fix}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add frontend/src/components/ClusterView.tsx
git commit -m "feat: add ClusterView expandable card grid"
```

---

## Phase 6: Frontend — Dashboard and Page Sections

### Task 18: Dashboard View (Core Interactive Panel)

**Files:**
- Create: `frontend/src/dashboard/Dashboard.tsx`
- Create: `frontend/src/dashboard/UserSidebar.tsx`
- Create: `frontend/src/dashboard/UserPanel.tsx`

**Step 1: Implement UserSidebar**

```tsx
// frontend/src/dashboard/UserSidebar.tsx
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { UserSummary } from "../api/types";

interface UserSidebarProps {
  selectedId: string | null;
  onSelect: (id: string) => void;
  initialScenario?: string;
}

export function UserSidebar({ selectedId, onSelect, initialScenario }: UserSidebarProps) {
  const [search, setSearch] = useState("");
  const [scenario, setScenario] = useState(initialScenario || "");

  const { data: users = [] } = useQuery({
    queryKey: ["users", scenario],
    queryFn: () => api.getUsers(scenario ? { scenario } : undefined),
  });

  const filtered = users.filter(
    (u) =>
      u.name.toLowerCase().includes(search.toLowerCase()) ||
      u.email.toLowerCase().includes(search.toLowerCase())
  );

  const riskBadge = (u: UserSummary) => {
    const maxScore = Math.max(u.churn_score || 0, u.fraud_score || 0);
    if (maxScore >= 70) return "bg-red-500";
    if (maxScore >= 40) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="w-72 border-r border-gray-800 flex flex-col h-full bg-gray-950">
      <div className="p-3 border-b border-gray-800 space-y-2">
        <input
          type="text"
          placeholder="Search users..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-blue-500"
        />
        <select
          value={scenario}
          onChange={(e) => setScenario(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm text-gray-200"
        >
          <option value="">All Scenarios</option>
          <option value="churn">Churn</option>
          <option value="fraud">Fraud</option>
          <option value="confused">Confused</option>
          <option value="normal">Normal</option>
        </select>
      </div>
      <div className="flex-1 overflow-y-auto">
        {filtered.map((user) => (
          <button
            key={user.user_id}
            onClick={() => onSelect(user.user_id)}
            className={`w-full text-left px-3 py-2.5 border-b border-gray-800/50 hover:bg-gray-900 transition-colors ${
              selectedId === user.user_id ? "bg-gray-900 border-l-2 border-l-blue-500" : ""
            }`}
          >
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${riskBadge(user)}`} />
              <span className="text-sm font-medium text-gray-200 truncate">{user.name}</span>
            </div>
            <div className="text-xs text-gray-500 mt-0.5 ml-4">{user.email}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

**Step 2: Implement UserPanel**

```tsx
// frontend/src/dashboard/UserPanel.tsx
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import { RiskGauge } from "../components/RiskGauge";
import { TimelineView } from "../components/TimelineView";
import { ExplanationPanel } from "../components/ExplanationPanel";
import { ActionCard } from "../components/ActionCard";
import { FeatureImportanceChart } from "../components/FeatureImportanceChart";

interface UserPanelProps {
  userId: string;
}

export function UserPanel({ userId }: UserPanelProps) {
  const { data: user } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => api.getUser(userId),
  });

  const { data: timeline } = useQuery({
    queryKey: ["timeline", userId],
    queryFn: () => api.getTimeline(userId, { limit: 200 }),
  });

  if (!user) return <div className="flex-1 flex items-center justify-center text-gray-600">Loading...</div>;

  const churnRisk = user.risk_scores.find((r) => r.score_type === "churn");
  const fraudRisk = user.risk_scores.find((r) => r.score_type === "fraud");
  const primaryRisk = (churnRisk?.score || 0) >= (fraudRisk?.score || 0) ? churnRisk : fraudRisk;

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-100">{user.name}</h2>
          <p className="text-sm text-gray-500">
            {user.email} &middot; {user.account_type} &middot; Joined{" "}
            {new Date(user.created_at).toLocaleDateString()}
          </p>
        </div>
        <span className="text-xs font-mono bg-gray-800 text-gray-400 px-2 py-1 rounded">
          {user.scenario_tag}
        </span>
      </div>

      {/* Risk Gauges */}
      <div className="flex gap-8">
        {churnRisk && <RiskGauge label="Churn Risk" score={churnRisk.score} />}
        {fraudRisk && <RiskGauge label="Fraud Risk" score={fraudRisk.score} />}
      </div>

      {/* Timeline */}
      {timeline && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wider mb-2">
            Event Timeline ({timeline.total} events)
          </h3>
          <TimelineView events={timeline.events} />
        </div>
      )}

      {/* Explanation + Action */}
      {primaryRisk && (
        <div className="grid md:grid-cols-2 gap-4">
          <ExplanationPanel risk={primaryRisk} />
          <div className="space-y-4">
            <ActionCard action={primaryRisk.recommended_action} score={primaryRisk.score} />
            <FeatureImportanceChart features={primaryRisk.top_features} />
          </div>
        </div>
      )}
    </div>
  );
}
```

**Step 3: Implement Dashboard container**

```tsx
// frontend/src/dashboard/Dashboard.tsx
import { useState } from "react";
import { UserSidebar } from "./UserSidebar";
import { UserPanel } from "./UserPanel";

interface DashboardProps {
  initialScenario?: string;
}

export function Dashboard({ initialScenario }: DashboardProps) {
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);

  return (
    <div className="flex h-[700px] border border-gray-800 rounded-xl overflow-hidden bg-gray-950">
      <UserSidebar
        selectedId={selectedUserId}
        onSelect={setSelectedUserId}
        initialScenario={initialScenario}
      />
      {selectedUserId ? (
        <UserPanel userId={selectedUserId} />
      ) : (
        <div className="flex-1 flex items-center justify-center text-gray-600">
          Select a user to inspect
        </div>
      )}
    </div>
  );
}
```

**Step 4: Commit**

```bash
git add frontend/src/dashboard/
git commit -m "feat: add interactive dashboard with sidebar, user panel, and risk views"
```

---

### Task 19: Portfolio Narrative Sections

**Files:**
- Create: `frontend/src/sections/Hero.tsx`
- Create: `frontend/src/sections/WhySection.tsx`
- Create: `frontend/src/sections/ScenariosSection.tsx`
- Create: `frontend/src/sections/ArchitectureSection.tsx`
- Create: `frontend/src/sections/TechStackSection.tsx`
- Create: `frontend/src/sections/Footer.tsx`

**Step 1: Implement all sections**

These are presentational components with Framer Motion scroll animations. Each section is self-contained. Implement them per the design: Hero with animated counters, Why with problem statement, Scenarios with 3 clickable cards, Architecture with pipeline diagram, TechStack grid, Footer with links.

> Note: Full JSX for each section is straightforward Tailwind + Framer Motion markup. The key integration point is ScenariosSection passing a `scrollToDashboard(scenario)` callback that smooth-scrolls to the Dashboard and sets its filter.

**Step 2: Commit**

```bash
git add frontend/src/sections/
git commit -m "feat: add portfolio narrative sections (hero, why, scenarios, architecture, tech, footer)"
```

---

### Task 20: Assemble Full Page in App.tsx

**Files:**
- Modify: `frontend/src/App.tsx`

**Step 1: Wire everything together**

```tsx
// frontend/src/App.tsx
import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "./api/client";
import { Dashboard } from "./dashboard/Dashboard";
import { Hero } from "./sections/Hero";
import { WhySection } from "./sections/WhySection";
import { ScenariosSection } from "./sections/ScenariosSection";
import { ArchitectureSection } from "./sections/ArchitectureSection";
import { TechStackSection } from "./sections/TechStackSection";
import { Footer } from "./sections/Footer";

function App() {
  const dashboardRef = useRef<HTMLDivElement>(null);
  const [dashboardScenario, setDashboardScenario] = useState<string | undefined>();

  const { data: stats } = useQuery({
    queryKey: ["stats"],
    queryFn: api.getStats,
  });

  const scrollToDashboard = (scenario?: string) => {
    setDashboardScenario(scenario);
    dashboardRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <Hero stats={stats} onTryDemo={() => scrollToDashboard()} />
      <WhySection />
      <ScenariosSection onExplore={scrollToDashboard} />

      <section ref={dashboardRef} className="max-w-7xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-bold mb-6">Live Dashboard</h2>
        <Dashboard initialScenario={dashboardScenario} />
      </section>

      <ArchitectureSection />
      <TechStackSection />
      <Footer />
    </div>
  );
}

export default App;
```

**Step 2: Verify frontend builds**

```bash
cd "C:/Users/King Hratch/intentguard/frontend"
npm run build
# Expected: Build succeeds
```

**Step 3: Commit**

```bash
git add frontend/src/App.tsx
git commit -m "feat: assemble full scrollable page with embedded dashboard"
```

---

## Phase 7: Integration and Polish

### Task 21: Docker Compose Full Stack

**Files:**
- Modify: `docker-compose.yml`

**Step 1: Update docker-compose for full stack with seed step**

```yaml
version: "3.9"

services:
  seed:
    build: ./backend
    command: >
      sh -c "cd /app/data && python seed.py && python train_models.py"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./backend:/app

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    depends_on:
      seed:
        condition: service_completed_successfully

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

**Step 2: Test full stack**

```bash
cd "C:/Users/King Hratch/intentguard"
docker-compose up --build
# Expected: seed runs, backend starts on :8000, frontend on :5173
```

**Step 3: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: docker-compose full stack with seed, backend, frontend"
```

---

### Task 22: End-to-End Smoke Test

**Files:**
- Create: `tests/test_e2e.py`

**Step 1: Write E2E smoke test**

```python
# tests/test_e2e.py
"""Run with backend + frontend up: python -m pytest tests/test_e2e.py -v"""
import requests

BASE = "http://localhost:8000/api"


def test_health():
    assert requests.get(f"{BASE}/health").status_code == 200


def test_users_list():
    r = requests.get(f"{BASE}/users")
    assert r.status_code == 200
    users = r.json()
    assert len(users) == 50


def test_user_detail():
    users = requests.get(f"{BASE}/users").json()
    uid = users[0]["user_id"]
    r = requests.get(f"{BASE}/users/{uid}")
    assert r.status_code == 200
    assert "risk_scores" in r.json()


def test_timeline():
    users = requests.get(f"{BASE}/users").json()
    uid = users[0]["user_id"]
    r = requests.get(f"{BASE}/users/{uid}/timeline")
    assert r.status_code == 200
    assert "events" in r.json()


def test_clusters():
    r = requests.get(f"{BASE}/insights/clusters")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_stats():
    r = requests.get(f"{BASE}/stats/overview")
    data = r.json()
    assert data["total_users"] == 50
    assert data["cluster_count"] == 3
```

**Step 2: Run (requires running backend)**

```bash
cd "C:/Users/King Hratch/intentguard"
python -m pytest tests/test_e2e.py -v
# Expected: all PASS
```

**Step 3: Commit**

```bash
git add tests/
git commit -m "test: add E2E smoke tests for all API endpoints"
```

---

### Task 23: Final README and Cleanup

**Files:**
- Modify: `README.md`

**Step 1: Update README with full documentation**

Expand README with: project overview, screenshots section (placeholder), quick start (docker-compose), development setup (manual backend + frontend), API docs link, architecture overview, tech stack, and license.

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: expand README with full project documentation"
```

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1 | 1-3 | Project scaffolding (git, backend, frontend) |
| 2 | 4-6 | Simulated data model, generators, seed script |
| 3 | 7-9 | ML pipeline (features, models, training) |
| 4 | 10-11 | Backend API routes |
| 5 | 12-17 | Frontend core components |
| 6 | 18-20 | Dashboard + portfolio page assembly |
| 7 | 21-23 | Docker, E2E tests, README |

**Total: 23 tasks across 7 phases.**
