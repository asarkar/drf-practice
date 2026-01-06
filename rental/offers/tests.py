from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Offer

User = get_user_model()


class OfferListViewTests(APITestCase):
    """Tests for OfferListView."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.offer = Offer.objects.create(
            address="123 Main St",
            size="2BR",
            property_type="APT",
            price=1500,
            text="Nice apartment",
            author=self.user,
        )

    def test_list_offers_unauthenticated(self) -> None:
        """Test that anyone can list offers."""
        url = reverse("offers:offer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_offer_authenticated(self) -> None:
        """Test that authenticated users can create offers."""
        self.client.force_authenticate(user=self.user)
        url = reverse("offers:offer-list")
        data = {
            "address": "456 Oak Ave",
            "size": "1BR",
            "property_type": "H",
            "price": 2000,
            "text": "Cozy house",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)
        # Verify author is automatically set to the authenticated user
        new_offer = Offer.objects.get(address="456 Oak Ave")
        self.assertEqual(new_offer.author, self.user)

    def test_create_offer_unauthenticated(self) -> None:
        """Test that unauthenticated users cannot create offers."""
        url = reverse("offers:offer-list")
        data = {
            "address": "456 Oak Ave",
            "size": "1BR",
            "property_type": "H",
            "price": 2000,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Offer.objects.count(), 1)


class OfferDetailViewTests(APITestCase):
    """Tests for OfferDetailView."""

    def setUp(self) -> None:
        """Set up test data."""
        self.author = User.objects.create_user(username="author", password="testpass")
        self.other_user = User.objects.create_user(username="other", password="testpass")
        self.offer = Offer.objects.create(
            address="123 Main St",
            size="2BR",
            property_type="APT",
            price=1500,
            text="Nice apartment",
            author=self.author,
        )

    def test_retrieve_offer_unauthenticated(self) -> None:
        """Test that anyone can retrieve an offer."""
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["address"], "123 Main St")

    def test_update_offer_as_author(self) -> None:
        """Test that the author can update their offer."""
        self.client.force_authenticate(user=self.author)
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        data = {
            "address": "789 New St",
            "size": "3BR",
            "property_type": "H",
            "price": 2500,
            "text": "Updated",
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.address, "789 New St")
        self.assertEqual(self.offer.price, 2500)

    def test_update_offer_as_non_author(self) -> None:
        """Test that non-authors cannot update an offer."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        data = {
            "address": "Hacked",
            "size": "1BR",
            "property_type": "APT",
            "price": 0,
            "text": "Hacked",
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.address, "123 Main St")

    def test_update_offer_unauthenticated(self) -> None:
        """Test that unauthenticated users cannot update an offer."""
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        data = {"address": "Hacked", "size": "1BR", "property_type": "APT", "price": 0}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_as_author(self) -> None:
        """Test that the author can delete their offer."""
        self.client.force_authenticate(user=self.author)
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)

    def test_delete_offer_as_non_author(self) -> None:
        """Test that non-authors cannot delete an offer."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Offer.objects.count(), 1)

    def test_delete_offer_unauthenticated(self) -> None:
        """Test that unauthenticated users cannot delete an offer."""
        url = reverse("offers:offer-detail", kwargs={"pk": self.offer.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Offer.objects.count(), 1)

    def test_retrieve_nonexistent_offer(self) -> None:
        """Test retrieving an offer that doesn't exist."""
        url = reverse("offers:offer-detail", kwargs={"pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserListViewTests(APITestCase):
    """Tests for UserListView."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")

    def test_list_users(self) -> None:
        """Test listing all users."""
        url = reverse("offers:user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class UserDetailViewTests(APITestCase):
    """Tests for UserDetailView."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.offer = Offer.objects.create(
            address="123 Main St",
            author=self.user,
        )

    def test_retrieve_user(self) -> None:
        """Test retrieving a user."""
        url = reverse("offers:user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertIn(self.offer.pk, response.data["offers"])

    def test_retrieve_nonexistent_user(self) -> None:
        """Test retrieving a user that doesn't exist."""
        url = reverse("offers:user-detail", kwargs={"pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
