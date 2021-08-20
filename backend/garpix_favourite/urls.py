from django.urls import path, include

from .routers import router

urlpatterns = [
    # favorites/ LIST, CREATE
    # favorites/{pk}/ DELETE
    # favorites/current/ LIST

    path('', include(router.urls))
]
