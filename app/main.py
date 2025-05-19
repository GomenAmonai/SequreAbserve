from fastapi import FastAPI, Request
from time import time
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from loguru import logger
from app.core.db import lifespan
from app.api import api_router

app = FastAPI(title="VPN API", lifespan=lifespan, docs_url="/")

app.include_router(api_router)

# Access-log
@app.middleware("http")
async def log_mw(request: Request, call_next):
    t0 = time()
    resp = await call_next(request)
    logger.info("%s %s → %s %d ms",
                request.method, request.url.path,
                resp.status_code, int((time()-t0)*1000))
    return resp

# unified errors
@app.exception_handler(HTTPException)
async def http_err(_, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def val_err(_, exc):
    return JSONResponse({"detail": exc.errors()}, status_code=422)

@app.exception_handler(Exception)
async def unhandled(_, exc):
    logger.exception("unhandled")
    return JSONResponse({"detail": "internal error"}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok"}