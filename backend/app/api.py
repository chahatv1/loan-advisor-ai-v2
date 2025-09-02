# app/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from .schemas import PredictRequest, PredictResponse
from .model import predict

# backend/app/api.py
from starlette.responses import RedirectResponse
@app.get("/", include_in_schema=False)
def root(): return RedirectResponse(url="/docs")

app = FastAPI(
    title="Loan Advisor API",
    version="0.1.0",
    description="Minimal API for loan approval demo. Swap the model later without breaking the contract.",
)

@app.get("/version")
def version(): return {"version": "0.1.0"}

# CORS so your future frontend can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict_route(req: PredictRequest):
    approved, probability, reasons = predict(
        income=req.income,
        loan_amount=req.loan_amount,
        tenure_months=req.tenure_months,
        age=req.age,
        credit_score=req.credit_score,
    )
    return PredictResponse(approved=approved, probability=probability, reasons=reasons)
