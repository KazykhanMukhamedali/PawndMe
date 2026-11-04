from django.shortcuts import get_object_or_404
from PIL import Image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from accounts.permissions import IsAdopter, IsShelterStaff, is_shelter_staff
from .models import Animal, AnimalPhoto, Favorite
from .serializers import AnimalInputSerializer, AnimalSerializer

MAX_PHOTO_SIZE = 5 * 1024 * 1024
MAX_PHOTOS = 5


def check_photos(photos, required):
    errors = []
    if required and len(photos) == 0:
        errors.append('Add at least 1 photo')
    if len(photos) > MAX_PHOTOS:
        errors.append('You can add up to 5 photos')
    for photo in photos:
        file_name = photo.name.lower()
        if not (file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png')):
            errors.append(photo.name + ': only JPG and PNG files are allowed')
        elif photo.size > MAX_PHOTO_SIZE:
            errors.append(photo.name + ': file is larger than 5 MB')
        else:
            try:
                Image.open(photo).verify()
                photo.seek(0)
            except Exception:
                errors.append(photo.name + ': this file is not a valid image')
    return errors


def save_photos(animal, photos):
    for photo in photos:
        AnimalPhoto.objects.create(animal=animal, image=photo)


def animal_response(animal, request):
    return AnimalSerializer(animal, context={'request': request}).data


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def animal_list_create(request):
    if request.method == 'GET':
        animals = Animal.objects.all().select_related('shelter').prefetch_related('photos')
        search = request.query_params.get('search', '').strip()
        animal_type = request.query_params.get('type', '').strip()
        size = request.query_params.get('size', '').strip()
        age_group = request.query_params.get('age_group', '').strip()
        personality = request.query_params.get('personality', '').strip()
        location = request.query_params.get('location', '').strip()

        if search != '':
            animals = animals.filter(name__icontains=search)
        if animal_type != '':
            animals = animals.filter(type=animal_type)
        if size != '':
            animals = animals.filter(size=size)
        if personality != '':
            animals = animals.filter(personality=personality)
        if location != '':
            animals = animals.filter(location__iexact=location)
        if age_group == 'up_to_1':
            animals = animals.filter(age__lte=1)
        elif age_group == '1_3':
            animals = animals.filter(age__gte=2, age__lte=3)
        elif age_group == '4_7':
            animals = animals.filter(age__gte=4, age__lte=7)
        elif age_group == '8_plus':
            animals = animals.filter(age__gte=8)

        data = AnimalSerializer(animals, many=True, context={'request': request}).data
        return Response({'count': len(data), 'results': data})

    if not is_shelter_staff(request.user):
        return Response({'detail': 'Only shelter staff can create animal profiles'}, status=403)

    serializer = AnimalInputSerializer(data=request.data)
    photos = request.FILES.getlist('photos')
    errors = {}

    if not serializer.is_valid():
        errors.update(serializer.errors)

    photo_errors = check_photos(photos, required=True)
    if photo_errors:
        errors['photos'] = photo_errors

    if errors:
        return Response(errors, status=400)

    animal = serializer.save(shelter=request.user.shelter)
    save_photos(animal, photos)
    return Response(animal_response(animal, request), status=201)


@api_view(['GET'])
def animal_locations(request):
    cities = Animal.objects.values_list('location', flat=True).distinct().order_by('location')
    return Response(list(cities))


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    if request.method == 'GET':
        return Response(animal_response(animal, request))

    if not is_shelter_staff(request.user) or animal.shelter_id != request.user.shelter_id:
        return Response({'detail': 'You can change only the animals of your shelter'}, status=403)

    if request.method == 'DELETE':
        animal.delete()
        return Response(status=204)

    serializer = AnimalInputSerializer(animal, data=request.data, partial=True)
    photos = request.FILES.getlist('photos')
    errors = {}

    if not serializer.is_valid():
        errors.update(serializer.errors)

    photo_errors = check_photos(photos, required=False)
    if photo_errors:
        errors['photos'] = photo_errors

    if errors:
        return Response(errors, status=400)

    serializer.save()
    if len(photos) > 0:
        animal.photos.all().delete()
        save_photos(animal, photos)

    return Response(animal_response(animal, request))


@api_view(['PATCH'])
@permission_classes([IsShelterStaff])
def animal_status(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.shelter_id != request.user.shelter_id:
        return Response({'detail': 'You can change only the animals of your shelter'}, status=403)

    new_status = str(request.data.get('status', ''))
    if new_status not in ['available', 'reserved', 'adopted']:
        return Response({'status': ['Choose available, reserved or adopted']}, status=400)

    animal.status = new_status
    animal.save()
    return Response(animal_response(animal, request))


@api_view(['GET'])
@permission_classes([IsShelterStaff])
def my_animals(request):
    animals = Animal.objects.filter(shelter=request.user.shelter)
    data = AnimalSerializer(animals, many=True, context={'request': request}).data
    return Response({'count': len(data), 'results': data})


@api_view(['GET'])
@permission_classes([IsAdopter])
def favorite_list(request):
    animals = []
    favorites = Favorite.objects.filter(user=request.user).select_related('animal')
    for favorite in favorites:
        animals.append(favorite.animal)
    data = AnimalSerializer(animals, many=True, context={'request': request}).data
    return Response({'count': len(data), 'results': data})


@api_view(['POST', 'DELETE'])
@permission_classes([IsAdopter])
def favorite_toggle(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    if request.method == 'POST':
        favorite, created = Favorite.objects.get_or_create(user=request.user, animal=animal)
        if created:
            return Response({'detail': 'Added to favorites'}, status=201)
        return Response({'detail': 'Already in favorites'}, status=200)

    Favorite.objects.filter(user=request.user, animal=animal).delete()
    return Response(status=204)