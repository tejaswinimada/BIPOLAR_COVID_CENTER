from django.db import models
from common.models import VaccinationCenter
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    
    
class SlotBooking(models.Model):
    STATUS_CHOICES = [
        ('done', 'Done'),
        ('not_done', 'Not Done'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE, related_name='slot_bookings')

    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not_done')

    class Meta:
        unique_together = ('center', 'date', 'time_slot', 'user')  # Ensure a user can't book the same slot twice

    def __str__(self):
        return f"{self.user.your_name} - {self.center.name} - {self.date} - {self.time_slot}"
