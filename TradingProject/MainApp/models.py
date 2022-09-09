from django.db import models

# Create your models here.
class csv(models.Model):
    csv_file=models.FileField(blank=True)
    timeframe=models.IntegerField()

