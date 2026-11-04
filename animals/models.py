from django.conf import settings
from django.db import models

from accounts.models import Shelter


class Animal(models.Model):
    TYPES = [('dog', 'Dog'), ('cat', 'Cat'), ('other', 'Other')]
    SIZES = [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')]
    PERSONALITIES = [('calm', 'Calm'), ('active', 'Active'), ('friendly', 'Friendly'), ('shy', 'Shy')]
    STATUSES = [('available', 'Available'), ('reserved', 'Reserved'), ('adopted', 'Adopted')]

    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='animals')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPES)
    age = models.PositiveSmallIntegerField(help_text='Age in years, 0 means younger than 1 year')
    size = models.CharField(max_length=10, choices=SIZES)
    location = models.CharField(max_length=100, help_text='City')
    personality = models.CharField(max_length=10, choices=PERSONALITIES, blank=True)
    health_info = models.TextField(blank=True)
    description = models.CharField(max_length=1000, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class AnimalPhoto(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='animals/')

    class Meta:
        ordering = ['id']


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'animal'], name='unique_favorite'),
        ]
        ordering = ['-created_at']