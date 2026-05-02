from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

from app.api.predict import router as predict_router
from app.monitoring.metrics import router as metrics_router
from app.monitoring.middleware import metrics_middleware


app = FastAPI(
    title="Transaction Fraud Model API",
    version="1.0.0",
    description="Production-style dummy fraud prediction service.",
)

app.middleware("http")(metrics_middleware)

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error for %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": "An unexpected error occurred. Please try again later.",
            }
        },
    )


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


app.include_router(predict_router)
app.include_router(metrics_router)
