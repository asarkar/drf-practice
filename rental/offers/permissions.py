from django.views.generic import View
from rest_framework import permissions
from rest_framework.request import Request

from .models import Offer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Offer) -> bool:
        return request.method in permissions.SAFE_METHODS or obj.author == request.user
