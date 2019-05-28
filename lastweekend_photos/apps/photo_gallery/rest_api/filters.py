import django_filters
from django_filters import rest_framework as filters

from apps.photo_gallery.models import Photo, Event, PhotoTag, PhotoPeople


class EventFilter(filters.FilterSet):

    class Meta:
        model = Event
        fields = '__all__'


class PhotoTagFilter(filters.FilterSet):

    class Meta:
        model = PhotoTag
        fields = '__all__'


class PhotoPeopleFilter(filters.FilterSet):

    class Meta:
        model = PhotoPeople
        fields = '__all__'


class PhotoFilter(filters.FilterSet):

    class Meta:
        model = Photo
        exclude = ('low_res_file', 'original_file', 'preview_file')
