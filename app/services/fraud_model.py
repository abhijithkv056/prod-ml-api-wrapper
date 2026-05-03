class ModelInferenceError(Exception):
    pass    

async def predict_fraud_probability(transaction_amount: float) -> float:
    return 0.85 if float(transaction_amount).is_integer() and (int(transaction_amount) % 2 == 1) else 0.15