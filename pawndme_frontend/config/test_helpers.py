import io

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import Shelter, User


def make_png(name='dog.png'):
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), 'white').save(buffer, format='PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


def make_adopter(email='anna@mail.com'):
    return User.objects.create_user(username=email, email=email, password='password123', account_type='adopter')


def make_staff(email='staff@mail.com', shelter_name='Happy Paws', city='Almaty'):
    shelter, created = Shelter.objects.get_or_create(name=shelter_name, city=city)
    return User.objects.create_user(username=email, email=email, password='password123',
                                    account_type='shelter_staff', shelter=shelter)


def client_for(user):
    client = APIClient()
    token, created = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


def animal_form(**changes):
    data = {
        'name': 'Bella',
        'type': 'dog',
        'age': 3,
        'size': 'small',
        'location': 'Almaty',
        'personality': 'calm',
        'health_info': 'Vaccinated',
        'description': 'Very friendly dog',
        'photos': make_png(),
    }
    data.update(changes)
    return data