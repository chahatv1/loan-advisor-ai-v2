# backend/app/model.py
import os
from math import exp
try:
    import joblib
except Exception:
    joblib = None

_model = None
_path = os.path.join("ai","models","model.pkl")
if joblib and os.path.exists(_path):
    _model = joblib.load(_path)

def _sigmoid(x): return 1/(1+exp(-x))

def predict(income, loan_amount, tenure_months, age, credit_score):
    if _model:
        X = [[income, loan_amount, tenure_months, age, credit_score]]
        proba = float(_model.predict_proba(X)[0][1])
        return proba >= 0.5, round(proba,3), ["model-based"]
    # fallback heuristic (kept simple)
    monthly = income/12.0; emi = loan_amount/max(tenure_months,1)
    credit_norm = (credit_score-300)/600
    z = 1.2*credit_norm + 1.0*((monthly-0.6*emi)/max(monthly,1))
    p = max(0.01, min(0.99, _sigmoid(z)))
    reasons = []
    if credit_norm>0.7: reasons.append("strong credit")
    if monthly>1.5*emi: reasons.append("affordable EMI")
    if not reasons: reasons.append("high risk ratio")
    return p>=0.5, round(p,3), reasons[:3]
