from django.urls import path

from subjects.views import TeacherSubjectView, TeacherPostCreationView

urlpatterns = [
    path('<int:pk>/teacher', TeacherSubjectView.as_view(), name='teacher_subject'),
    path('<int:pk>/teacher/post_create', TeacherPostCreationView.as_view(), name='post_create_teacher'),
]
