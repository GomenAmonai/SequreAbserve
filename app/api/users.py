from fastapi import APIRouter, HTTPException
from app.repository import user_repo
from app.models.user import UserOut
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=201)
async def create_user():
    data = await user_repo.create_user()
    return data

@router.get("/{user_id}/config")
async def user_config(user_id: UUID):
    row = await user_repo.get_user(str(user_id))
    if not row:
        raise HTTPException(404, "user not found")
    wg_priv, wg_pub, ss_pwd, active = row
    if not active:
        raise HTTPException(402, "subscription not active")
    return {
        "wireguard": f"...{wg_priv}...",
        "shadowsocks2022": f"ss://2022-blake3-aes-256-gcm:{ss_pwd}@host:8443#vpn",
        "vless": f"vless://{user_id}@host:443?...",
    }