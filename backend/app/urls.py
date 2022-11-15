from garpixcms.urls import *  # noqa
from garpix_user.views import LoginView, LogoutView

urlpatterns = [
    # garpix_user
    path('', include(('garpix_user.urls', 'user'), namespace='garpix_user')),
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="authorize"),

    # garpix_favourite
    path('', include(('garpix_favourite.urls', 'favourite'), namespace='garpix_favourite')),
] + urlpatterns
