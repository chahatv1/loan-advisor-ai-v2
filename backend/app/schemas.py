from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    income: float = Field(..., ge=0)
    loan_amount: float = Field(..., gt=0)
    tenure_months: int = Field(..., gt=0)
    age: int = Field(..., ge=18, le=100)
    credit_score: int = Field(..., ge=300, le=900)

class PredictResponse(BaseModel):
    approved: bool
    probability: float
    reasons: list[str]
