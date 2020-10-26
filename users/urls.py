from django.urls import path

from . import views
from .views import UserProfileView
from django.conf.urls import include, url


urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]
