from django.utils.functional import cached_property

from rest_framework import serializers


class FavoriteMixin:
    """
        Миксин для моделей,
        которые планируются добавляться в избранное.
    """

    @cached_property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self) -> str:
        # К примеру: return reverse('view-detail', args=[self.id])

        raise NotImplementedError()


class FavoriteSerializerMixin(serializers.Serializer):
    """
        Миксин для наследования всех сериализаторов,
        которые планируются добавляться в избранное.
    """
    model_name = serializers.CharField(
        read_only=True, max_length=100
    )
