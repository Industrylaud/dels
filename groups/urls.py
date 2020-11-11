from django.urls import path

from .views import GroupView, PostView

from . import views


urlpatterns = [
    path('mygroup/', GroupView.as_view(), name='student_group'),
    path('mygroup/post/<int:pk>', PostView.as_view(), name='post_detail')
]
