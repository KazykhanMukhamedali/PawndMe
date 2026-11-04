from django.contrib.auth.models import AbstractUser
from django.db import models


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'city'], name='unique_shelter_name_city'),
        ]

    def __str__(self):
        return f'{self.name} ({self.city})'


class User(AbstractUser):
    ADOPTER = 'adopter'
    SHELTER_STAFF = 'shelter_staff'
    ACCOUNT_TYPES = [
        (ADOPTER, 'Adopter'),
        (SHELTER_STAFF, 'Shelter staff'),
    ]

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default=ADOPTER)
    # Only shelter staff have a shelter
    shelter = models.ForeignKey(Shelter, null=True, blank=True, on_delete=models.SET_NULL, related_name='staff')

    def __str__(self):
        return self.email