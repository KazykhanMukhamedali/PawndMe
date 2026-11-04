from rest_framework.permissions import BasePermission


def is_adopter(user):
    return user.is_authenticated and user.account_type == 'adopter'


def is_shelter_staff(user):
    return user.is_authenticated and user.account_type == 'shelter_staff' and user.shelter is not None


class IsAdopter(BasePermission):
    message = 'Only adopters can do this.'

    def has_permission(self, request, view):
        return is_adopter(request.user)


class IsShelterStaff(BasePermission):
    message = 'Only shelter staff can do this.'

    def has_permission(self, request, view):
        return is_shelter_staff(request.user)