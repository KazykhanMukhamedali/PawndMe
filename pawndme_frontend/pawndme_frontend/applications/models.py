from django.conf import settings
from django.db import models

from animals.models import Animal


class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.CharField(max_length=500, help_text='Living conditions and pet experience')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'animal'], name='unique_application'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name + ' for ' + self.animal.name