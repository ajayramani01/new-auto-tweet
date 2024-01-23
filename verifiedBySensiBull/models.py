from django.db import models

# Create your models here.
class verifiedUser(models.Model):
    verification_url=models.URLField(max_length=200, unique=True)
    name=models.CharField(max_length=150)
    x_username=models.CharField(max_length=50)
    totalPL=models.CharField(max_length=20)
    ROI=models.CharField(max_length=20)
    total_capital=models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)

