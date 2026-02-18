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
