from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from garpix_user.models import UserSession


class Favorite(models.Model):
    """
        Модель "Избранное" для пользователя.
    """

    user_session = models.ForeignKey(
        UserSession, on_delete=models.CASCADE, verbose_name=_('User'),
        related_name='favorites'
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Object ID')
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_('Content type')
    )
    content_object = GenericForeignKey(
        'content_type', 'object_id'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )

    @property
    def entity(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    @classmethod
    def get_favorite_by_request(cls, request):
        user_session = UserSession.get_from_request(request)
        elements = Favorite.objects.filter(
            user_session=user_session
        )

        return elements

    @classmethod
    def get_entity_by_request(cls, request, obj_id, model_name):
        """
        Will return the favorite entities for the current user or None
        """
        elements = cls.get_favorite_by_request(request)
        model_type = ContentType.objects.filter(model=model_name).first()
        if model_type is None:
            return None
        el = elements.filter(
            object_id=obj_id,
            content_type__pk=model_type.pk,
        ).first()

        return el

    def __str__(self):
        return 'User session %i | Favorite: %s %s' % (
            self.user_session.id, self.object_id, self.content_object.__class__.__name__
        )

    class Meta:
        ordering = ('id',)
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        unique_together = (('user_session', 'content_type', 'object_id'),)
