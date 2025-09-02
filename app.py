import streamlit as st
import pandas as pd
import joblib

# ---------------------------
# Load Model & Encoders
# ---------------------------
model = joblib.load("rf_churn_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# ---------------------------
# Page Config & Custom CSS
# ---------------------------
st.set_page_config(page_title="Telco Customer Churn Predictor", layout="wide")

# Add background & custom styles
st.markdown(
    """
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #0F172A, #1E293B, #2563EB);

        font-family: 'Segoe UI', sans-serif;
    }

    

    /* Title Styling */
    .title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #2563EB;
        margin-bottom: 10px;
    }

    /* Form labels */
    label {
        font-weight: 600 !important;
    }

    /* Prediction results */
    .prediction-box {
        text-align: center;
        font-size: 1.3rem;
        padding: 1rem;
        border-radius: 12px;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# App Layout
# ---------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h1 class="title">📊 Telco Customer Churn Predictor</h1>', unsafe_allow_html=True)
st.write("Fill out the customer details below and click **Predict** to see whether the customer is likely to churn.")

# ---------------------------
# Input Form
# ---------------------------
with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=72, value=12)
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=70.0)
        total_charges = st.number_input("Total Charges", min_value=0.0, value=1000.0)
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

    with col2:
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ])

    submitted = st.form_submit_button("🔍 Predict Churn")

# ---------------------------
# Prediction Logic
# ---------------------------
if submitted:
    # Build DataFrame from user input
    input_df = pd.DataFrame([{
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }])

    # Apply saved encoders to categorical columns
    for col, le in label_encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform(input_df[col])

    # Predict
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.markdown(
            f'<div class="prediction-box" style="background:#ffebee; color:#b71c1c;">'
            f'⚠️ <b>High Risk:</b> This customer is likely to churn.<br>'
            f'<b>Probability:</b> {prediction_proba:.2%}'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="prediction-box" style="background:#e8f5e9; color:#1b5e20;">'
            f'✅ <b>Low Risk:</b> This customer is unlikely to churn.<br>'
            f'<b>Probability:</b> {prediction_proba:.2%}'
            '</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
