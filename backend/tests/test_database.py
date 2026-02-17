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
