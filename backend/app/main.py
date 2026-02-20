from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.users import router as users_router
from app.api.insights import router as insights_router
from app.api.stats import router as stats_router

DB_PATH = str(Path(__file__).parent.parent / "data" / "intentguard.db")


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
