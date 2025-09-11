import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def LGBM_regressor(facility_name: str, data: pd.DataFrame):
    
    filtered = data[data["facility_name"] == facility_name].dropna(
        subset=["co2_emitted_tonnes", "region", "storage_site_type", "season", "co2_captured_tonnes"]
    )

    if filtered.empty:
        raise ValueError(f"No valid data found for facility {facility_name}")

    
    features = filtered[["co2_emitted_tonnes", "region", "storage_site_type", "season"]].copy()
    target   = filtered["co2_captured_tonnes"]

    
    categorical_cols = ["region", "storage_site_type", "season"]
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        features[col] = le.fit_transform(features[col].astype(str))
        encoders[col] = le  # saving encoders for later predictions

    
    training_data = lgb.Dataset(features, label=target, categorical_feature=categorical_cols)

    # Parameters
    params = {
        "objective": "regression",
        "metric": "rmse",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "verbose": -1
    }

    # Train model on all available data
    model = lgb.train(params, training_data, num_boost_round=200)

    return model, encoders
