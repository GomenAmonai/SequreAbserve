import uuid, aiosqlite
from app.core.db import get_pool
from app.core import crypto

wg_priv, wg_pub = crypto.gen_wg_keypair()
ss_pwd = crypto.gen_ss_password()

async def create_user() -> dict:
    uid = str(uuid.uuid4())
    wg_priv, wg_pub = "priv", "pub"  # ← заглушка: подставьте генератор
    ss_pwd = "pwd"

    pool = get_pool()
    await pool.execute(
        "INSERT INTO users (id,wg_priv,wg_pub,ss_pwd) VALUES (?,?,?,?)",
        (uid, wg_priv, wg_pub, ss_pwd),
    )
    await pool.commit()
    return {"id": uid, "wg_private": wg_priv, "wg_public": wg_pub, "ss_password": ss_pwd}

async def activate(uid: str) -> None:
    pool = get_pool()
    await pool.execute("UPDATE users SET active=1 WHERE id=?", (uid,))
    await pool.commit()

async def get_user(uid: str) -> tuple | None:
    pool = get_pool()
    cur = await pool.execute(
        "SELECT wg_priv,wg_pub,ss_pwd,active FROM users WHERE id=?", (uid,)
    )
    return await cur.fetchone()