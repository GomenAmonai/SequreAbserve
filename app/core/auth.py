from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from app.core.config import settings

ALGORITHM = "HS256"
TOKEN_TTL  = timedelta(hours=12)
security = HTTPBearer()

def create_token(sub: str) -> str:
    payload = {"sub": sub, "exp": datetime.utcnow() + TOKEN_TTL}
    return jwt.encode(payload, settings.stripe_webhook_secret or "dev-secret", ALGORITHM)

def parse_token(credentials=Depends(security)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.stripe_webhook_secret or "dev-secret", [ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")