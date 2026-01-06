from django.urls import path

from .views import OfferDetails, OfferList, UserDetails, UserList

urlpatterns = [
    path("offers/", OfferList.as_view(), name="offer-list"),
    path("offers/<int:pk>/", OfferDetails.as_view(), name="offer-detail"),
    path("users/", UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetails.as_view(), name="user-detail"),
]
