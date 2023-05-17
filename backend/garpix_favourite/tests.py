import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Favorite
from garpix_user.models import UserSession

User = get_user_model()


class FavoriteTestCase(APITestCase):
    def setUp(self) -> None:
        self.password = '12345'
        self.username = 'test'

        self.username2 = 'test2'

        self.user = User.objects.create_user(username=self.username, email='user@site.com', password=self.password)
        self.user2 = User.objects.create_user(username=self.username2, email='user2@site.com', password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.favorite_url = reverse('garpix_favourite:favorite-list')
        self.favorite_url_user = reverse('garpix_favourite:favorite-get-user-favorites')

        session_key = uuid.uuid4()

        self.header = {'HTTP_USER_SESSION_TOKEN': str(session_key)}

        self.user_session = UserSession.objects.create(user=self.user, token_number=session_key)
        model_type = ContentType.objects.get_for_model(User)

        self.favorite = Favorite.objects.create(
            user_session=self.user_session,
            object_id=self.user.pk,
            content_type=model_type
        )

    def test_entity(self):
        self.assertEqual(self.favorite.entity.pk, self.user.pk)

    def test_create_favorite(self):
        settings.ACCEPTED_FAVORITE_MODELS += ['User']

        data = {
            'object_id': self.user2.pk,
            'model_name': 'User'
        }

        response = self.client.post(self.favorite_url, data=data, **self.header)
        response_json = response.json()
        print(response_json, 'response_json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_list(self):
        settings.ACCEPTED_FAVORITE_MODELS += ['User']

        response = self.client.get(self.favorite_url_user, **self.header)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
