import aiosqlite, contextlib, asyncio
from app.core.config import settings

DB_PATH = settings.db_path

_SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
    id          TEXT PRIMARY KEY,
    email       TEXT,
    wg_priv     TEXT,
    wg_pub      TEXT,
    ss_pwd      TEXT,
    active      INTEGER DEFAULT 0,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS nodes (
    id          TEXT PRIMARY KEY,
    ip          TEXT,
    country     TEXT,
    wg_port     INTEGER,
    ss_port     INTEGER,
    vless_port  INTEGER,
    load        INTEGER DEFAULT 0
);
"""

_pool: aiosqlite.Connection | None = None


async def init_db() -> None:
    global _pool
    _pool = await aiosqlite.connect(DB_PATH)
    await _pool.executescript(_SCHEMA)
    await _pool.commit()


def get_pool() -> aiosqlite.Connection:
    if _pool is None:
        raise RuntimeError("DB not initialised")
    return _pool


@contextlib.asynccontextmanager
async def lifespan(app):
    await init_db()
    try:
        yield
    finally:
        await _pool.close()