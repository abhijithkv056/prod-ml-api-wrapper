"""Dummy fraud model inference logic."""


class ModelInferenceError(Exception):
    """Raised when the fraud model fails to produce a prediction."""


async def predict_fraud_probability(transaction_amount: float) -> float:
    """Return fraud probability based on odd/even whole-number amount."""
    try:
        if float(transaction_amount).is_integer() and (int(transaction_amount) % 2 == 1):
            return 0.85
        return 0.15
    except Exception as exc:
        raise ModelInferenceError(
            f"Model inference failed for amount={transaction_amount}: {exc}"
        ) from exc
