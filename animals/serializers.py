from rest_framework import serializers

from applications.models import Application
from .models import Animal, Favorite


class AnimalInputSerializer(serializers.ModelSerializer):
    """Checks the data that shelter staff send when they create or edit a profile."""

    class Meta:
        model = Animal
        fields = ['name', 'type', 'age', 'size', 'location', 'personality', 'health_info', 'description']


class AnimalSerializer(serializers.ModelSerializer):
    """Animal data that we send to React. The request must be passed in the context."""
    photos = serializers.SerializerMethodField()
    shelter = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    has_applied = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ['id', 'name', 'type', 'age', 'size', 'location', 'personality', 'health_info',
                  'description', 'status', 'status_label', 'photos', 'shelter',
                  'is_favorite', 'has_applied', 'created_at']

    def get_photos(self, animal):
        request = self.context['request']
        urls = []
        for photo in animal.photos.all():
            urls.append(request.build_absolute_uri(photo.image.url))
        return urls

    def get_shelter(self, animal):
        return {'id': animal.shelter.id, 'name': animal.shelter.name, 'city': animal.shelter.city}

    def get_status_label(self, animal):
        return animal.get_status_display()

    def get_is_favorite(self, animal):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, animal=animal).exists()

    def get_has_applied(self, animal):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Application.objects.filter(user=user, animal=animal).exists()