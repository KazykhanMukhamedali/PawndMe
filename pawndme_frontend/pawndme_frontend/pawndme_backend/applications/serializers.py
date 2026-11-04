from rest_framework import serializers
from .models import Application


class ApplicationInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['full_name', 'phone', 'email', 'message']


class ApplicationSerializer(serializers.ModelSerializer):
    animal = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'animal', 'full_name', 'phone', 'email', 'message', 'created_at']

    def get_animal(self, application):
        return {'id': application.animal.id, 'name': application.animal.name}