from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class URL(models.Model):
    original = models.URLField(max_length=600)
    short = models.CharField(max_length=100)