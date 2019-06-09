from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
CHOICES = (
    ('c', 'Common'),
    ('p', 'Premium')
    )


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(default='users/default.png', upload_to='users/')
    subsctiption = models.CharField(max_length=1, choices=CHOICES, default='c')
    subsctiption_due = models.DateField(null=True, blank=True)



