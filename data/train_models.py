import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import aiosqlite
from app.ml.features import extract_user_features
from app.ml.scoring import ChurnModel, FraudModel

DEFAULT_DB = str(Path(__file__).parent / "intentguard.db")
MODELS_DIR = Path(__file__).parent.parent / "models"


async def train_and_save(db_path: str = DEFAULT_DB):
    MODELS_DIR.mkdir(exist_ok=True)

    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row

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

        churn_model = ChurnModel()
        churn_model.train(features_list, churn_labels)
        churn_model.save(str(MODELS_DIR / "churn_model.pkl"))
        print(f"Churn model saved ({sum(churn_labels)}/{len(churn_labels)} positive)")

        fraud_model = FraudModel()
        fraud_model.train(features_list)
        fraud_model.save(str(MODELS_DIR / "fraud_model.pkl"))
        print(f"Fraud model saved (trained on {len(features_list)} users)")

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
