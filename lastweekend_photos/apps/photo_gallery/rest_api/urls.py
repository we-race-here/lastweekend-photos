from django.urls import include, path
from rest_framework import routers

from apps.photo_gallery.rest_api.views import SessionView, ProfileView

rest_router = routers.DefaultRouter()
rest_router.trailing_slash = "/?"  # added to support both / and slashless
rest_router.register(r'session', SessionView, basename='session')
rest_router.register(r'me', ProfileView, basename='profile')

app_name = 'photo_gallery'
urlpatterns = [
    path('', include(rest_router.urls))
]
