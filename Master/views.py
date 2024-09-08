from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .serializers import HousingDataSerializer
from .models import HousingData
from .utils import (
    load_model,
    prepare_data,
    update_prediction_value,
    predict_house_value,
)

MODEL_NAME = "model.joblib"
TRAIN_DATA = "housing.csv"


class PredictHouseValueView(generics.ListCreateAPIView):
    queryset = HousingData.objects.all().order_by("-id")
    serializer_class = HousingDataSerializer

    def create(self, request, *args, **kwargs):

        model = load_model(MODEL_NAME)

        X_train, _, _, _ = prepare_data(TRAIN_DATA)
        X_train_columns = X_train.columns

        serializer = HousingDataSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            longitude = data["longitude"]
            latitude = data["latitude"]
            housing_median_age = data["housing_median_age"]
            total_rooms = data["total_rooms"]
            total_bedrooms = data["total_bedrooms"]
            population = data["population"]
            households = data["households"]
            median_income = data["median_income"]
            ocean_proximity = data["ocean_proximity"]

            prediction = predict_house_value(
                longitude=longitude,
                latitude=latitude,
                housing_median_age=housing_median_age,
                total_rooms=total_rooms,
                total_bedrooms=total_bedrooms,
                population=population,
                households=households,
                median_income=median_income,
                ocean_proximity=ocean_proximity,
                model=model,
                X_train_columns=X_train_columns,
            )
            instance = serializer.save()
            saved_id = instance.id

            update_prediction_value(saved_id, prediction)
            return Response(
                {"predicted_value": prediction}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
