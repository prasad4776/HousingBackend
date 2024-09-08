from django.db import models

# Create your models here.


class HousingData(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    housing_median_age = models.FloatField()
    total_rooms = models.FloatField()
    total_bedrooms = models.FloatField()
    population = models.FloatField()
    households = models.FloatField()
    median_income = models.FloatField()
    ocean_proximity = models.CharField()
    creation_date = models.DateTimeField()
    predicted_value = models.FloatField(null=True)

    def __str__(self):
        return self.ocean_proximity
