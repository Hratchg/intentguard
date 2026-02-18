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

        users = generate_users(count=50, seed=42)
        await db.executemany(
            "INSERT INTO users (user_id, name, email, created_at, account_type, scenario_tag) VALUES (?, ?, ?, ?, ?, ?)",
            [(u["user_id"], u["name"], u["email"], u["created_at"], u["account_type"], u["scenario_tag"]) for u in users],
        )

        all_events = []
        for user in users:
            all_events.extend(generate_events_for_user(user))
        await db.executemany(
            "INSERT INTO events (event_id, user_id, timestamp, event_type, properties) VALUES (?, ?, ?, ?, ?)",
            [(e["event_id"], e["user_id"], e["timestamp"], e["event_type"], e["properties"]) for e in all_events],
        )

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
