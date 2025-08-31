from src.loan_advisor.baseline import Application, score, explain

def demo():
    app = Application(
        income=60000/12,      # monthly income
        loan_amount=400000,   # requested loan amount
        term_months=36,
        credit_score=720,
        existing_debt=8000
    )
    s = score(app)
    reasons = explain(app, s)

    print(f"Baseline score: {s:.2f}")
    print("Reasons:")
    for r in reasons:
        print(f"- {r}")

if __name__ == "__main__":
    demo()