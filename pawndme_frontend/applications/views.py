from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsAdopter, IsShelterStaff
from animals.models import Animal
from .models import Application
from .serializers import ApplicationInputSerializer, ApplicationSerializer


@api_view(['POST'])
@permission_classes([IsAdopter])
def apply(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    if animal.status != 'available':
        return Response({'detail': 'This animal is not available for adoption'}, status=400)

    if Application.objects.filter(user=request.user, animal=animal).exists():
        return Response({'detail': 'You already applied'}, status=400)

    serializer = ApplicationInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save(user=request.user, animal=animal)
    return Response({'detail': 'Application sent'}, status=201)


@api_view(['GET'])
@permission_classes([IsShelterStaff])
def application_list(request):
    applications = Application.objects.filter(animal__shelter=request.user.shelter).select_related('animal')
    data = ApplicationSerializer(applications, many=True).data
    return Response({'count': len(data), 'results': data})