from django.urls import path

from . import views
from .views import UserProfileView
from django.conf.urls import include, url


urlpatterns = [
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.UserProfileView.as_view(), name='user_profile'),
]
