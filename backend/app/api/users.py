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
            FROM users u WHERE 1=1
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
            return {"error": "User not found"}
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
    request: Request, user_id: str,
    event_type: str | None = Query(None),
    limit: int = Query(100), offset: int = Query(0),
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
            "SELECT * FROM risk_scores WHERE user_id = ? ORDER BY computed_at DESC", (user_id,),
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
            "SELECT timestamp, event_type, properties FROM events WHERE user_id = ? ORDER BY timestamp", (user_id,),
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
