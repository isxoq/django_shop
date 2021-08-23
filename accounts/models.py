from django.db import models


# Create your models here.

class TempNumber(models.Model):
    phone = models.CharField(max_length=20)
    code = models.IntegerField()
    expire_at = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
