from django.urls import path, include

from .routers import router

urlpatterns = [
    # favorites/ CREATE
    # favorites/{pk}/ DELETE
    # favorites/current/ LIST

    path('', include(router.urls))
]
