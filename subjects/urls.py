from django.urls import path

from subjects.views import TeacherSubjectView

urlpatterns = [
    path('<int:pk>/teacher', TeacherSubjectView.as_view(), name='teacher_subject'),
]
