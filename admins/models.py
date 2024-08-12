from django.db import models

class Signup(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self) -> str:
        return self.username
