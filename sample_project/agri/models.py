from django.db import models

class District(models.Model):
    Name = models.CharField(max_length = 100)
    Humidity = models.IntegerField()
    Rainfall = models.IntegerField()
    Min_Temp = models.IntegerField()
    Max_Temp = models.IntegerField()

# Create your models here.

