from logging import getLogger

from typing import Optional

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Favorite

try:
    ACCEPTED_FAVORITE_MODELS = settings.ACCEPTED_FAVORITE_MODELS
except AttributeError:
    raise AttributeError(
        _('ACCEPTED_FAVORITE_MODELS не найдено в настройках.')
    )

logger = getLogger(__name__)


def _get_content_type_by_model_name(model_name: str) -> ContentType:
    model_name = model_name.lower()

    return ContentType.objects.get(model=model_name)


class FavoriteSerializer(serializers.ModelSerializer):
    """
        Сериализатор для избранного.
    """
    model_name = serializers.CharField(
        required=True, write_only=True, max_length=100
    )
    favorite_url = serializers.SerializerMethodField(
        read_only=True
    )

    def _get_request(self):
        return self.context.get('request')

    def get_favorite_url(self, instance) -> Optional[str]:
        """
            Возвращает полный путь до объекта content_object.
        """

        try:
            return self._get_request().build_absolute_uri(
                instance.content_object.get_absolute_url()
            )
        except AttributeError:
            logger.error(
                _(
                    'Модель "%s" не имеет get_absolute_url().\n'
                    'favorite_url будет обозначен, как None.\n'
                    'FavoriteMixin обязателен для использования.'
                    % instance.content_object.__class__.__name__
                )
            )
            return None

    def validate(self, attrs):
        user = self._get_request().user
        model_name = attrs['model_name']
        object_id = attrs['object_id']
        content_type = _get_content_type_by_model_name(model_name)
        model = self.Meta.model

        if model_class := content_type.model_class():
            if not model_class.objects.filter(id=object_id).exists():
                raise ValidationError(
                    {'error': _('%s with id %i does not exists.' % (model_name, object_id))}
                )

        if model.objects.filter(
                user=user,
                content_type=content_type,
                object_id=object_id
        ).exists():
            raise ValidationError(
                {'error': _('The object has already been added to favorites.')}
            )

        return attrs

    def validate_model_name(self, value):
        if value not in ACCEPTED_FAVORITE_MODELS:
            raise ValidationError(
                _('Model must be in: %s' % ', '.join(ACCEPTED_FAVORITE_MODELS))
            )
        return value

    def create(self, validated_data):
        model_name = validated_data.pop('model_name')
        content_type = _get_content_type_by_model_name(model_name)

        validated_data.update({
            'content_type': content_type
        })

        return super().create(validated_data)

    class Meta:
        model = Favorite
        exclude = ('user',)
