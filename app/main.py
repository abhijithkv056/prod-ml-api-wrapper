from __future__ import annotations

from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.metrics import router as metrics_router
from app.api.predict import router as predict_router
from app.core.errors import register_exception_handlers
from app.monitoring.middleware import metrics_middleware


app = FastAPI(
    title="Transaction Fraud Model API",
    version="1.0.0",
    description="Production-style dummy fraud prediction service.",
)

app.middleware("http")(metrics_middleware)
register_exception_handlers(app)

app.include_router(predict_router)
app.include_router(metrics_router)
app.include_router(health_router)
