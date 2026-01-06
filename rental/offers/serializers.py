from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Offer

User = get_user_model()


class OfferSerializer(serializers.ModelSerializer[Offer]):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Offer
        fields = ["id", "address", "size", "type", "price", "sharing", "text", "author"]
        read_only_fields = ["id"]


class UserSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    # `read_only=True` because `offers` is a reverse ForeignKey relationship (Offer.author -> User).
    # The User model doesn't have an "offers" column - it's a reverse lookup.
    # Offers belong to users via `Offer.author`, so they can't be assigned directly here.
    # This field outputs the user's offers but doesn't accept input.
    offers: serializers.PrimaryKeyRelatedField[Offer] = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "offers"]
        read_only_fields = ["id"]
