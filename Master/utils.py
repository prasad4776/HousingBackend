from .models import HousingData
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 100


def prepare_data(input_data_path):
    df = pd.read_csv(input_data_path)
    df = df.dropna()

    df = pd.get_dummies(df)

    df_features = df.drop(["median_house_value"], axis=1)
    y = df["median_house_value"].values

    X_train, X_test, y_train, y_test = train_test_split(
        df_features, y, test_size=0.2, random_state=RANDOM_STATE
    )

    return X_train, X_test, y_train, y_test


def load_model(filename):
    model = joblib.load(filename)
    return model


def predict_house_value(
    longitude,
    latitude,
    housing_median_age,
    total_rooms,
    total_bedrooms,
    population,
    households,
    median_income,
    ocean_proximity,
    model,
    X_train_columns,
):
    input_data = pd.DataFrame(
        {
            "longitude": [longitude],
            "latitude": [latitude],
            "housing_median_age": [housing_median_age],
            "total_rooms": [total_rooms],
            "total_bedrooms": [total_bedrooms],
            "population": [population],
            "households": [households],
            "median_income": [median_income],
            "ocean_proximity": [ocean_proximity],
        }
    )

    input_data = pd.get_dummies(input_data)

    missing_cols = set(X_train_columns) - set(input_data.columns)
    for c in missing_cols:
        input_data[c] = 0
    input_data = input_data[X_train_columns]

    prediction = model.predict(input_data)
    return prediction[0]


def update_prediction_value(saved_id, prediction):
    fetch_record = HousingData.objects.filter(id=saved_id)[0]
    fetch_record.predicted_value = prediction
    fetch_record.save()
    return fetch_record
