from fastapi import APIRouter
from .users import router as users_router
from .billing import router as billing_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(billing_router)