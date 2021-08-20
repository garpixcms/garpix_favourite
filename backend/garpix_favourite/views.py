from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    @action(methods=['GET'], detail=False, permission_classes=(IsAuthenticated,), url_path='current')
    def get_user_favorites(self, request):
        data = Favorite.objects.filter(user=request.user)
        serializer = self.get_serializer(data, many=True)

        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
