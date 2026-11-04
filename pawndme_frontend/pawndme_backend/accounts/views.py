from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Shelter, User


def user_data(user):
    shelter = None
    if user.shelter is not None:
        shelter = {'id': user.shelter.id, 'name': user.shelter.name, 'city': user.shelter.city}
    return {
        'id': user.id,
        'email': user.email,
        'account_type': user.account_type,
        'account_type_label': user.get_account_type_display(),
        'shelter': shelter,
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = str(request.data.get('email', '')).strip().lower()
    password = str(request.data.get('password', ''))
    account_type = str(request.data.get('account_type', 'adopter'))
    shelter_name = str(request.data.get('shelter_name', '')).strip()
    shelter_city = str(request.data.get('shelter_city', '')).strip()

    errors = {}
    if email == '' or '@' not in email:
        errors['email'] = ['Enter a valid email']
    elif User.objects.filter(username=email).exists():
        errors['email'] = ['Email is already registered']

    if len(password) < 8:
        errors['password'] = ['Password must have at least 8 characters']

    if account_type not in ['adopter', 'shelter_staff']:
        errors['account_type'] = ['Choose Adopter or Shelter staff']

    if account_type == 'shelter_staff':
        if shelter_name == '':
            errors['shelter_name'] = ['Enter the shelter name']
        if shelter_city == '':
            errors['shelter_city'] = ['Enter the shelter city']

    if errors:
        return Response(errors, status=400)

    user = User.objects.create_user(
        username=email, email=email, password=password, account_type=account_type
    )
    if account_type == 'shelter_staff':
        shelter, created = Shelter.objects.get_or_create(name=shelter_name, city=shelter_city)
        user.shelter = shelter
        user.save()

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': user_data(user)}, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = str(request.data.get('email', '')).strip().lower()
    password = str(request.data.get('password', ''))
    user = authenticate(username=email, password=password)
    if user is None:
        return Response({'detail': 'Wrong email or password'}, status=400)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': user_data(user)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'detail': 'Logged out'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(user_data(request.user))