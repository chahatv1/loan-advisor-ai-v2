import requests, streamlit as st
API = st.secrets.get("API_URL", "http://127.0.0.1:8000")
st.title("Loan Advisor")
with st.form("f"):
    income = st.number_input("Annual income", 0, step=1000)
    loan = st.number_input("Loan amount", 0, step=1000)
    tenure = st.number_input("Tenure (months)", 1, step=1, value=60)
    age = st.number_input("Age", 18, 100, value=25)
    credit = st.number_input("Credit score", 300, 900, value=720)
    s = st.form_submit_button("Predict")
if s:
    r = requests.post(f"{API}/predict", json=dict(
        income=income, loan_amount=loan, tenure_months=tenure, age=age, credit_score=credit))
    st.json(r.json() if r.ok else {"error": r.text})
