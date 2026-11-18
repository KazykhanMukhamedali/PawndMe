from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

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
@transaction.atomic
def register(request):
    email = str(request.data.get('email', '')).strip().lower()
    password = str(request.data.get('password', ''))
    account_type = str(request.data.get('account_type', 'adopter'))
    shelter_name = str(request.data.get('shelter_name', '')).strip()
    shelter_city = str(request.data.get('shelter_city', '')).strip()
    full_name = str(request.data.get('full_name', '')).strip()

    errors = {}
    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = ['Enter a valid email']
    if len(email) > 150:
        errors['email'] = ['Enter an email of at most 150 characters']
    elif 'email' not in errors and User.objects.filter(username=email).exists():
        errors['email'] = ['Email is already registered']
    if len(full_name) > 150:
        errors['full_name'] = ['Enter a name of at most 150 characters']

    if len(password) < 8:
        errors['password'] = ['Password must have at least 8 characters']

    if account_type not in ['adopter', 'shelter_staff']:
        errors['account_type'] = ['Choose Adopter or Shelter staff']

    if account_type == 'shelter_staff':
        if shelter_name == '':
            errors['shelter_name'] = ['Enter the shelter name']
        elif len(shelter_name) > 100:
            errors['shelter_name'] = ['Enter a shelter name of at most 100 characters']
        if shelter_city == '':
            errors['shelter_city'] = ['Enter the shelter city']
        elif len(shelter_city) > 100:
            errors['shelter_city'] = ['Enter a shelter city of at most 100 characters']

    if errors:
        return Response(errors, status=400)

    shelter = None
    if account_type == 'shelter_staff':
        shelter, created = Shelter.objects.get_or_create(name=shelter_name, city=shelter_city)
        if not created:
            return Response({'shelter_name': ['This shelter already exists. Contact an administrator for access.']}, status=400)

    user = User.objects.create_user(
        username=email, email=email, password=password, account_type=account_type,
        first_name=full_name, shelter=shelter,
    )

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


class PasswordResetThrottle(AnonRateThrottle):
    rate = '5/min'
    scope = 'password_reset'


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([PasswordResetThrottle])
def forgot_password(request):
    email = str(request.data.get('email', '')).strip().lower()
    user = User.objects.filter(username=email, is_active=True).first()
    if user and user.has_usable_password():
        query = urlencode({
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        url = f'{settings.FRONTEND_URL}/#/reset-password?{query}'
        send_mail('Reset your PawndMe password', f'Use this link to reset your password:\n\n{url}',
                  settings.DEFAULT_FROM_EMAIL, [user.email])
    return Response({'detail': 'If an account exists for that email, we sent a reset link.'})


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def reset_password(request):
    try:
        uid = int(urlsafe_base64_decode(str(request.data.get('uid', ''))))
        user = User.objects.select_for_update().filter(pk=uid, is_active=True).first()
    except (TypeError, ValueError, OverflowError):
        user = None
    token = str(request.data.get('token', ''))
    if user is None or not default_token_generator.check_token(user, token):
        return Response({'detail': 'This reset link is invalid or expired.'}, status=400)

    password = request.data.get('password')
    if not isinstance(password, str) or len(password) < 8:
        return Response({'password': ['Password must have at least 8 characters']}, status=400)

    user.set_password(password)
    user.save(update_fields=['password'])
    Token.objects.filter(user=user).delete()
    return Response({'detail': 'Password updated successfully'})
