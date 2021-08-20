from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class FavoriteTestCase(APITestCase):
    def setUp(self) -> None:
        self.password = '12345'
        self.username = 'test'

        self.user = User.objects.create_user(username=self.username, email='user@site.com', password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.favorite_url = reverse('favorite-list')

    def test_user_favorite_list_as_unauthorized(self):
        response = self.client.get(self.favorite_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_create_favorite_as_authorized(self):
        settings.ACCEPTED_FAVORITE_MODELS += ['User']
        self._make_authentication()

        data = {
            'object_id': 1,
            'model_name': 'User'
        }

        response = self.client.post(self.favorite_url, data=data)
        response_json = response.json()
        response_json.pop('created_at')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_json, {'id': 1, 'object_id': 1, 'favorite_url': None, 'content_type': 33})

    def test_create_favorite_as_unauthorized(self):
        response = self.client.post(self.favorite_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _make_authentication(self) -> None:
        if settings.ENABLE_GARPIX_AUTH:
            response = self.client.post(
                reverse('garpix_auth:api_login'),
                {
                    'username': self.username,
                    'password': self.password,
                },
                HTTP_ACCEPT='application/json'
            )

            access_token = response.json()['access_token']
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        else:
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
