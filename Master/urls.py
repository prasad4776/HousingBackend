from django.urls import path

from .views import PredictHouseValueView


urlpatterns = [
    path("predict/", PredictHouseValueView.as_view(), name="predict_house_value"),
]
