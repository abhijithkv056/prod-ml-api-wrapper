from __future__ import annotations

from fastapi import APIRouter, Response

from app.monitoring.metrics import generate_metrics_payload

router = APIRouter(tags=["monitoring"])


@router.get("/metrics")
async def metrics() -> Response:
    payload, media_type = generate_metrics_payload()
    return Response(content=payload, media_type=media_type)
