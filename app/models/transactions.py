from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserLocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_amount: float = Field(..., gt=0)
    merchant_id: str = Field(..., min_length=1, max_length=128)
    transaction_time: datetime
    user_location: UserLocation


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction: Transaction


class PredictResponse(BaseModel):
    fraud_probability: float = Field(..., ge=0, le=1)
    model: Literal["dummy_rule_v1"] = "dummy_rule_v1"


class BatchPredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transactions: list[Transaction] = Field(..., min_length=1, max_length=100)


class BatchPredictResponse(BaseModel):
    predictions: list[PredictResponse]
    model: Literal["dummy_rule_v1"] = "dummy_rule_v1"
