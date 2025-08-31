# Super simple heuristic model you can replace later with a real one.
# Keep interfaces the same so the API code doesn’t change.

from math import exp

REASON_MAP = {
    "credit": "strong credit",
    "emi": "affordable EMI",
    "income": "sufficient income",
    "risk": "high risk ratio",
}

def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))

def predict(income: float, loan_amount: float, tenure_months: int, age: int, credit_score: int):
    # naive affordability: monthly income vs EMI
    monthly_income = income / 12.0
    emi = loan_amount / max(tenure_months, 1)
    affordability = (monthly_income - 0.6 * emi) / max(monthly_income, 1)

    # normalize credit score to ~0..1
    credit_norm = (credit_score - 300) / 600  # 300..900 -> 0..1

    # simple linear mix -> probability
    z = 1.2 * credit_norm + 1.0 * affordability + 0.1 * (age >= 21) - 0.2 * (loan_amount > 25 * income)
    prob = max(0.01, min(0.99, sigmoid(z)))

    reasons = []
    if credit_norm > 0.7: reasons.append(REASON_MAP["credit"])
    if monthly_income > 1.5 * emi: reasons.append(REASON_MAP["emi"])
    if income > 500000: reasons.append(REASON_MAP["income"])
    if not reasons:
        reasons.append(REASON_MAP["risk"])

    approved = prob >= 0.5
    return approved, float(round(prob, 3)), reasons[:3]
