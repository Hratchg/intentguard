from fastapi import APIRouter, Request
import aiosqlite

router = APIRouter()


@router.get("/stats/overview")
async def overview(request: Request):
    db_path = request.app.state.db_path
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
