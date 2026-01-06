from django.urls import path

from .views import OfferDetailView, OfferListView, UserDetailView, UserListView

app_name = "offers"

urlpatterns = [
    path("offers/", OfferListView.as_view(), name="offer-list"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
