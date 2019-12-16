from django.conf.urls import url

from .views import *

app_name = 'user'

urlpatterns = [
    url(r'^register/$', UserRegisterView.as_view(), name='user_register'),
    url(r'^login/$', UserLoginView.as_view(), name='user_login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='user_logout'),
    url(r'^get/(?P<key>[-:\w]+)$', UserGetView.as_view(), name='user_get'),
    url(r'^setCoins/$', UserSetCoinsView.as_view(), name='user_set_coins'),
    url(r'^getUsers/', UserGetUsersView.as_view(), name='user_get_users'),
]
