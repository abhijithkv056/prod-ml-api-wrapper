

class ModelInferenceError(Exception):


    async def predict_fraud_probability(transaction_amount: float) -> float:
     try:
         if float(transaction_amount).is_integer() and (int(transaction_amount) % 2 == 1):
            return 0.85
         return 0.15
     except Exception as exc:
        raise ModelInferenceError(
            f"Model inference failed for amount={transaction_amount}: {exc}"
        ) from exc
