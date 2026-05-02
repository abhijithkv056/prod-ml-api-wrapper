"""Dummy fraud model inference logic."""


async def predict_fraud_probability(transaction_amount: float) -> float:
    """Return fraud probability based on odd/even whole-number amount."""
    if float(transaction_amount).is_integer() and (int(transaction_amount) % 2 == 1):
        return 0.85
    return 0.15
