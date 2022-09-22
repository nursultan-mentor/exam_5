from rest_framework.permissions import BasePermission, SAFE_METHODS


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.profile.is_sender:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.profile.is_sender:
            return True
        else:
            return False


class ItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.profile.is_sender:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        print(request.user.profile, obj.profile)
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.profile.is_sender and obj.profile == request.user.profile:
            return True
        else:
            return False


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.profile and not request.user.profile.is_sender:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.profile and not request.user.profile.is_sender and obj.profile == request.user.profile:
            return True
        else:
            return False
