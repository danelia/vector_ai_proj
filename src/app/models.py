from django.db import models

class Continent(models.Model): 
    continent_id                = models.AutoField(primary_key=True)

    continent_name              = models.TextField(blank=False, null=False)

    continent_population        = models.IntegerField()

    continent_area              = models.FloatField()

class Country(models.Model):
    country_id                  = models.AutoField(primary_key=True)

    continent                   = models.ForeignKey(Continent, on_delete=models.CASCADE)

    country_name                = models.TextField(blank=False, null=False)

    country_population          = models.IntegerField()

    country_area                = models.FloatField()

    country_n_hospitals         = models.IntegerField()

    country_n_national_parks    = models.IntegerField()

class City(models.Model):
    city_id                     = models.AutoField(primary_key=True)

    continent                   = models.ForeignKey(Continent, on_delete=models.CASCADE)
    
    country                     = models.ForeignKey(Country, on_delete=models.CASCADE)

    city_name                   = models.TextField(blank=False, null=False)

    city_population             = models.IntegerField()

    city_area                   = models.FloatField()

    city_n_roads                = models.IntegerField()

    city_n_trees                = models.IntegerField()