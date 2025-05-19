from fastapi import APIRouter
from app.core import db

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/")
def summary():
    conn = db.get_conn()
    rows = conn.execute("SELECT id, active FROM users").fetchall()
    conn.close()
    return [{"id": r[0], "active": bool(r[1])} for r in rows]