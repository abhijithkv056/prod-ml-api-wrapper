from __future__ import annotations

from fastapi import APIRouter

from app.models.transactions import (
    BatchPredictRequest,
    BatchPredictResponse,
    PredictRequest,
    PredictResponse,
)
from app.services.fraud_model import predict_fraud_probability


router = APIRouter(tags=["predictions"])


@router.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    probability = await predict_fraud_probability(req.transaction.transaction_amount)
    return PredictResponse(fraud_probability=probability)


@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch(req: BatchPredictRequest) -> BatchPredictResponse:
    predictions = [
        PredictResponse(
            fraud_probability=await predict_fraud_probability(t.transaction_amount)
        )
        for t in req.transactions
    ]
    return BatchPredictResponse(predictions=predictions)
