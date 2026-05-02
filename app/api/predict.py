from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.transactions import (
    BatchPredictRequest,
    BatchPredictResponse,
    PredictRequest,
    PredictResponse,
)
from app.services.fraud_model import ModelInferenceError, predict_fraud_probability

logger = logging.getLogger(__name__)

router = APIRouter(tags=["predictions"])


@router.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    try:
        probability = await predict_fraud_probability(req.transaction.transaction_amount)
        return PredictResponse(fraud_probability=probability)
    except ModelInferenceError as exc:
        logger.error("Inference error on /predict: %s", exc)
        return JSONResponse(
            status_code=503,
            content={"error": {"type": "model_error", "message": str(exc)}},
        )


@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch(req: BatchPredictRequest) -> BatchPredictResponse:
    predictions: list[PredictResponse] = []
    for t in req.transactions:
        try:
            probability = await predict_fraud_probability(t.transaction_amount)
            predictions.append(PredictResponse(fraud_probability=probability))
        except ModelInferenceError as exc:
            logger.error("Inference error on /predict/batch for amount=%s: %s", t.transaction_amount, exc)
            return JSONResponse(
                status_code=503,
                content={"error": {"type": "model_error", "message": str(exc)}},
            )
    return BatchPredictResponse(predictions=predictions)
