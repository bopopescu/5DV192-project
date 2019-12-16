from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=32, null=False, blank=False, unique=True)
    password = models.CharField(max_length=1024, null=False, blank=False, unique=False)
    coins = models.PositiveIntegerField(default=100000, null=False, blank=False)
    date_registered = models.DateTimeField(default=timezone.now)


class UserSession(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=256, null=False, blank=False, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
