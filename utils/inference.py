from utils.HouseData import HouseData
import pandas as pd


def predict_new(data: HouseData, preprocessor, model):
    # to DF
    df = pd.DataFrame([data.model_dump()])

    # feature engineering (must match what was done in the training notebook)
    df["rooms_per_household"] = df["total_rooms"] / df["households"]
    df["bedroms_per_rooms"] = df["total_bedrooms"] / df["total_rooms"]
    df["population_per_household"] = df["population"] / df["households"]

    # transform
    X_processed = preprocessor.transform(df)

    # predict
    y_pred = model.predict(X_processed)

    return {"predicted_price": float(y_pred[0])}
