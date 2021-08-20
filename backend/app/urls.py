from garpixcms.urls import *  # noqa

urlpatterns = [path('api/v1/', include('garpix_favourite.urls'))] + urlpatterns
