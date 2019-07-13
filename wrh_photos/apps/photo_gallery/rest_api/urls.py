from django.urls import include, path
from rest_framework import routers

from apps.photo_gallery.rest_api.views import SessionView, ProfileView, EventView, PhotoView, PhotoTagView, \
    PhotoPeopleView

rest_router = routers.DefaultRouter()
rest_router.trailing_slash = "/?"  # added to support both / and slashless
rest_router.register(r'session', SessionView, basename='session')
rest_router.register(r'me', ProfileView, basename='profile')
rest_router.register(r'event', EventView)
rest_router.register(r'photo', PhotoView)
rest_router.register(r'photo_tag', PhotoTagView)
rest_router.register(r'photo_people', PhotoPeopleView)

app_name = 'photo_gallery'
urlpatterns = [
    path('', include(rest_router.urls))
]
