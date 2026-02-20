from django.db import models

class TempUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    otp=models.CharField(max_length=6)

    def __str__(self):
        return self.name