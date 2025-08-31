# File moved to src/loan_advisor/baseline.py

from dataclasses import dataclass

@dataclass
class Application:
    income: float           # monthly income
    loan_amount: float      # requested loan amount
    term_months: int        # loan term in months
    credit_score: int       # 300-850
    existing_debt: float    # total monthly debt payments

def score(app: Application) -> float:
    
    if app.term_months <= 0 or app.income <= 0 or app.loan_amount <= 0:
        return 0.0

    # debt-to-income ratio
    dti = (app.existing_debt) / max(app.income, 1e-6)

    # basic affordability: how big is the loan vs income
    size = app.loan_amount / (app.income * 12)

    # normalize credit score to 0..1
    cs = (app.credit_score - 300) / 550
    cs = min(max(cs, 0), 1)

    # weighted mashup
    raw = 0.55 * cs + 0.25 * (1 - min(dti, 2.0)/2.0) + 0.20 * (1 - min(size, 2.0)/2.0)

    # clamp just in case your inputs are chaos
    return max(0.0, min(1.0, raw))

def explain(app: Application, s: float) -> list[str]:
    """
    Returns human-readable reasons for the score.
    """
    reasons = []
    dti = (app.existing_debt) / max(app.income, 1e-6)
    size = app.loan_amount / (app.income * 12)

    if app.credit_score >= 750:
        reasons.append("Strong credit score helps.")
    elif app.credit_score >= 650:
        reasons.append("Decent credit score.")
    else:
        reasons.append("Low credit score limits approval odds.")

    if dti <= 0.35:
        reasons.append("Healthy debt-to-income ratio.")
    elif dti <= 0.5:
        reasons.append("DTI is borderline; lenders may be cautious.")
    else:
        reasons.append("High debt-to-income ratio hurts approval chances.")

    if size <= 0.8:
        reasons.append("Requested amount is reasonable vs annual income.")
    elif size <= 1.2:
        reasons.append("Loan size is somewhat high compared to income.")
    else:
        reasons.append("Loan size is very high compared to income.")

    if s >= 0.7:
        reasons.append("Overall profile looks favorable.")
    elif s >= 0.4:
        reasons.append("Mixed factors; approval possible with conditions.")
    else:
        reasons.append("Low baseline score; consider lowering amount or improving credit.")

    return reasons

# New file src/loan_advisor/__init__.py
# (empty file)