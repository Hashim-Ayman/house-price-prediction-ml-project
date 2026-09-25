# 🏡 California House Price Predictor

🔗 **Live App:** [(https://your-app-url.streamlit.app](https://house-price-prediction-ml-project-dw98wvkhy785aeafdobejs.streamlit.app/))]

A machine learning web app that predicts the median house value for a California census block, built on the classic **California Housing** dataset. The app is powered by an **XGBoost regression model** and served through an interactive **Streamlit** interface.

> Enter block-level details — location, housing characteristics, and median income — and get an instant price estimate, complete with a live map preview.

---

## ✨ Features

- **Interactive prediction UI** — sliders and inputs grouped into clear sections (Location, Block characteristics, Income)
- **Live map preview** — see exactly where the block you're describing sits on the map as you adjust latitude/longitude
- **Real-time inference** — model and preprocessing pipeline loaded once at startup for fast predictions
- **Reproducible pipeline** — the same feature engineering used during training is applied automatically at inference time

---

## 🧠 Model Overview

| | |
|---|---|
| **Algorithm** | XGBoost Regressor |
| **Task** | Regression — predicts `median_house_value` (USD) |
| **Dataset** | California Housing dataset (20,640 census block records) |
| **Preprocessing** | `ColumnTransformer` — median imputation + standard scaling (numerical), constant imputation + one-hot encoding (categorical) |

### Input features

| Feature | Description |
|---|---|
| `longitude`, `latitude` | Geographic coordinates of the block |
| `housing_median_age` | Median age of houses in the block |
| `total_rooms`, `total_bedrooms` | Total rooms / bedrooms in the block |
| `population`, `households` | Population and number of households |
| `median_income` | Median household income (tens of thousands USD) |
| `ocean_proximity` | Categorical proximity to the ocean (`<1H OCEAN`, `INLAND`, `NEAR OCEAN`, `NEAR BAY`, `ISLAND`) |

### Engineered features

Computed automatically at inference time from the raw inputs above, matching the feature engineering used during training:

- `rooms_per_household` = `total_rooms / households`
- `bedroms_per_rooms` = `total_bedrooms / total_rooms`
- `population_per_household` = `population / households`

---

## 📊 Model Comparison

Two candidate models were trained and tuned (`RandomizedSearchCV` for Random Forest, `GridSearchCV` for XGBoost), then evaluated once on a held-out test set:

| Model | Test RMSE ↓ | Test R² ↑ |
|---|---:|---:|
| Random Forest (tuned) | 61,541.66 | 0.711 |
| **XGBoost (tuned)** | **45,373.09** | **0.843** |

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** — web UI
- **XGBoost** — regression model
- **scikit-learn** — preprocessing pipeline (`ColumnTransformer`)
- **Pydantic** — input validation and schema
- **pandas** — data handling
- **python-dotenv** — environment configuration

---

## 📁 Project Structure

```
house-price-prediction/
├── Data/
│   └── housing.csv              # Training dataset
├── models/
│   ├── best_xgb.pkl              # Trained XGBoost model
│   └── preprocessor.pkl          # Fitted preprocessing pipeline
├── notebooks/
│   └── notebook.ipynb            # EDA, feature engineering & model training
├── utils/
│   ├── __init__.py
│   ├── config.py                  # Loads env vars and model artifacts
│   ├── HouseData.py                # Pydantic schema for input validation
│   └── inference.py                # Feature engineering + prediction logic
├── streamlit_app.py               # Streamlit application entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/house-price-prediction.git
cd house-price-prediction
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 3. Set up environment variables

Copy the example file and adjust values if needed:

```bash
cp .env.example .env
```

```env
APP_NAME=House Price Prediction
VERSION=1.0.0
```

### 4. Run the app

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## 🖼️ Demo

<<img width="1919" height="866" alt="Screenshot 2026-09-25 185811" src="https://github.com/user-attachments/assets/d2b2c308-09da-4075-8830-a00e9ec50343" />
>
<<img width="1919" height="1013" alt="Screenshot 2026-09-25 185923" src="https://github.com/user-attachments/assets/6a23caba-ce4d-48a6-a406-5dcb3e73fed2" />
>

---

## 📓 Notebook

The full data exploration, feature engineering, and model selection process (including comparison of candidate models) is documented in [`notebooks/notebook.ipynb`](notebooks/notebook.ipynb).

---

## 🙋 Author

Built by **[Hashim-Ayman]** — feel free to reach out or open an issue if you have questions or suggestions.
