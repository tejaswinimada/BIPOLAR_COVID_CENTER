from django.db import models
from users.models import*


class VaccinationCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    working_hours_start = models.CharField(max_length=255,null=True, blank=True)  # Start time
    working_hours_end = models.CharField(null=True, blank=True,max_length=255)   # End time
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class DosageDetail(models.Model):
    center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE, related_name='dosages')
    date = models.DateField()
    dose_count = models.IntegerField()  # Number of doses given on that date

    def __str__(self):
        return f"{self.center.name} - {self.date}"
