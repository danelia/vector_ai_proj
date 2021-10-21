from django.db import models

class Continent(models.Model): 
    id                = models.AutoField(primary_key=True)

    name              = models.TextField(blank=False, null=False)

    population        = models.IntegerField()

    area              = models.FloatField()

class Country(models.Model):
    id                  = models.AutoField(primary_key=True)

    continent           = models.ForeignKey(Continent, on_delete=models.CASCADE)

    name                = models.TextField(blank=False, null=False)

    population          = models.IntegerField()

    area                = models.FloatField()

    n_hospitals         = models.IntegerField()

    n_national_parks    = models.IntegerField()

class City(models.Model):
    id                     = models.AutoField(primary_key=True)
    
    country                = models.ForeignKey(Country, on_delete=models.CASCADE)

    name                   = models.TextField(blank=False, null=False)

    population             = models.IntegerField()

    area                   = models.FloatField()

    n_roads                = models.IntegerField()

    n_trees                = models.IntegerField()