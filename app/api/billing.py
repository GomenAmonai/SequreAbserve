from fastapi import APIRouter, Request, HTTPException
import stripe, hmac, hashlib
from app.core.config import settings
from app.repository import user_repo

router = APIRouter(prefix="/billing", tags=["billing"])
stripe.api_key = settings.stripe_key

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("Stripe-Signature", "")
    if settings.stripe_webhook_secret:
        try:
            stripe.Webhook.construct_event(payload, sig, settings.stripe_webhook_secret)
        except Exception:
            raise HTTPException(400, "invalid signature")
    event = request.json() if not settings.stripe_webhook_secret else stripe.Event.construct_from(request.json(), stripe.api_key)
    if event["type"] == "checkout.session.completed":
        uid = event["data"]["object"]["client_reference_id"]
        await user_repo.activate(uid)
    return {"received": True}