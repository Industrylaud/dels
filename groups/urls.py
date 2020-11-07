from django.urls import path

from .views import GroupView

from . import views


urlpatterns = [
    path('mygroup/', GroupView.as_view(), name='student_group')
]
