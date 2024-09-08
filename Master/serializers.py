from .models import HousingData
from rest_framework import serializers


class HousingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingData
        fields = "__all__"
