import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.photo_gallery.models import User


def create_user(username, password, **kwargs):
    kwargs.setdefault('first_name', 'F1')
    kwargs.setdefault('last_name', 'L1')
    kwargs.setdefault('email', '{}@email.com'.format(username))
    kwargs.setdefault('is_superuser', False)
    kwargs.setdefault('is_staff', False)
    kwargs['username'] = username
    user = User(**kwargs)
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def admin_user(request):
    return create_user('admin1', 'adminpass', is_superuser=True, is_staff=True)


@pytest.fixture
def api_client(request):
    return APIClient()


class TestSessionView(object):

    def rest_url(self, view_name):
        return reverse('photo_gallery_rest_api:{}'.format(view_name), kwargs={'version': 'v1'})

    @pytest.mark.django_db
    def test_get_session_no_login(self, admin_user, api_client):
        response = api_client.get(self.rest_url('session-list'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_session_logged_in(self, admin_user, api_client):
        api_client.post(self.rest_url('session-list'), {'username': admin_user.username, 'password': 'adminpass'})
        response = api_client.get(self.rest_url('session-list'))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data.get('id') is not None
        assert data.get('username') == admin_user.username
