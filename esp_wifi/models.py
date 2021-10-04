from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Esp(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Command(models.Model):
    name = models.CharField(max_length=100)
    esp = models.ForeignKey(Esp, on_delete=models.CASCADE)