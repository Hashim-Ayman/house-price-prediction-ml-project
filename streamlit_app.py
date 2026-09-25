"""
Streamlit app for the California house price prediction project.

Calls `predict_new` directly in-process (reusing the preprocessor/model
loaded in utils.config).

Run with:
    streamlit run streamlit_app.py
(from the project root)
"""

import streamlit as st
import pandas as pd

from utils.inference import predict_new
from utils.config import APP_NAME, VERSION, preprocessor, xgboost_model
from utils.HouseData import HouseData

st.set_page_config(
    page_title=APP_NAME or "House Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0f1720 0%, #131b24 100%);
        }

        .hero {
            padding: 1.75rem 2rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1.5rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2rem;
            color: #f5f7fa;
        }
        .hero p {
            margin: 0.35rem 0 0 0;
            color: #a9b4c0;
            font-size: 0.95rem;
        }

        .section-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.25rem 1.5rem 0.5rem 1.5rem;
            margin-bottom: 1.25rem;
        }
        .section-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #7fb8ff;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.75rem;
        }

        .result-card {
            padding: 1.75rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #14532d 0%, #0f3d22 100%);
            border: 1px solid rgba(120, 255, 170, 0.25);
            text-align: center;
        }
        .result-card .label {
            color: #9ee6b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .result-card .value {
            color: #f5fff8;
            font-size: 2.6rem;
            font-weight: 700;
            margin: 0.25rem 0;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <h1>🏡 {APP_NAME or "California House Price Predictor"}</h1>
        <p>Estimate median house value from block-level census features &nbsp;·&nbsp; v{VERSION or "1.0.0"}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.write(
        "This app predicts the median house value for a California "
        "census block using an XGBoost regression model trained on the "
        "classic California Housing dataset."
    )
    st.markdown("### 🧮 Model")
    st.write("**Algorithm:** XGBoost Regressor")
    st.write("**Target:** Median house value (USD)")
    st.divider()
    st.caption("Adjust the inputs, then click **Predict price**.")

# ----------------------------------------------------------------------------
# Input form
# ----------------------------------------------------------------------------
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    with st.form("prediction_form"):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">📍 Location</div>', unsafe_allow_html=True
        )
        c1, c2 = st.columns(2)
        with c1:
            latitude = st.slider("Latitude", 32.0, 42.0, 34.2, 0.01)
        with c2:
            longitude = st.slider("Longitude", -125.0, -113.0, -118.4, 0.01)
        ocean_proximity = st.selectbox(
            "Ocean proximity",
            ["<1H OCEAN", "INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"],
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">🏘️ Block characteristics</div>',
            unsafe_allow_html=True,
        )
        housing_median_age = st.slider("Median house age (years)", 1, 52, 29)
        c3, c4 = st.columns(2)
        with c3:
            total_rooms = st.number_input(
                "Total rooms", min_value=1.0, value=2127.0, step=10.0
            )
            population = st.number_input(
                "Population", min_value=1.0, value=1166.0, step=10.0
            )
        with c4:
            total_bedrooms = st.number_input(
                "Total bedrooms", min_value=1.0, value=435.0, step=5.0
            )
            households = st.number_input(
                "Households", min_value=1.0, value=409.0, step=5.0
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">💵 Income</div>', unsafe_allow_html=True
        )
        median_income = st.slider(
            "Median income (tens of thousands, USD)", 0.5, 15.0, 3.5, 0.1
        )
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("🔮 Predict price", use_container_width=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">🗺️ Block location</div>', unsafe_allow_html=True
    )
    st.map(
        pd.DataFrame({"lat": [latitude], "lon": [longitude]}),
        zoom=5,
        size=200,
        color="#7fb8ff",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    result_slot = st.empty()
    with result_slot.container():
        st.markdown(
            """
            <div class="section-card" style="text-align:center; color:#7a8699; padding:2.5rem 1rem;">
                Fill in the details and click <b>Predict price</b> to see an estimate here.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Prediction
# ----------------------------------------------------------------------------
if submitted:
    try:
        house = HouseData(
            longitude=longitude,
            latitude=latitude,
            housing_median_age=housing_median_age,
            total_rooms=total_rooms,
            total_bedrooms=total_bedrooms,
            population=population,
            households=households,
            median_income=median_income,
            ocean_proximity=ocean_proximity,
        )

        result = predict_new(data=house, preprocessor=preprocessor, model=xgboost_model)
        price = result.get("predicted_price")

        with result_slot.container():
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="label">Predicted median house value</div>
                    <div class="value">${price:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("Raw result"):
                st.json(result)

    except Exception as e:
        with result_slot.container():
            st.error("Something went wrong while predicting.")
            st.exception(e)
