from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.serializers import BaseSerializer

from .models import Offer
from .permissions import IsAuthorOrReadOnly
from .serializers import OfferSerializer, UserSerializer

User = get_user_model()


class OfferList(generics.ListCreateAPIView[Offer]):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: BaseSerializer[Offer]) -> None:
        serializer.save(author=self.request.user)


class OfferDetails(generics.RetrieveUpdateDestroyAPIView[Offer]):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    # IsAuthenticatedOrReadOnly implements has_permission() - checked before fetching the object
    # IsAuthorOrReadOnly implements has_object_permission() - checked after fetching the object
    # Without IsAuthenticatedOrReadOnly, an unauthenticated DELETE request would:
    # 1. Fetch the object from the database
    # 2. Then fail at has_object_permission
    # With both, it fails early at has_permission without the unnecessary database query.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class UserList(generics.ListAPIView):  # type: ignore[type-arg]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):  # type: ignore[type-arg]
    queryset = User.objects.all()
    serializer_class = UserSerializer
