from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

app_name = "tasks"

# Create a router and register our viewset
router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]
