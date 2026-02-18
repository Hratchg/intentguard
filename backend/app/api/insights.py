import json
from fastapi import APIRouter, Request
import aiosqlite

router = APIRouter()


@router.get("/insights/clusters")
async def list_clusters(request: Request):
    db_path = request.app.state.db_path
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
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM ux_clusters WHERE cluster_id = ?", (cluster_id,))
        row = await cursor.fetchone()
        if not row:
            return {"error": "Cluster not found"}
        cluster = {**dict(row), "example_messages": json.loads(row["example_messages"])}
    return cluster
