from django.urls import path

from subjects.views import TeacherSubjectView, TeacherPostCreationView, TeacherTaskCreationView

urlpatterns = [
    path('<int:pk>/teacher', TeacherSubjectView.as_view(), name='teacher_subject'),
    path('<int:pk>/teacher/post_create', TeacherPostCreationView.as_view(), name='post_create_teacher'),
    path('<int:pk>/teacher/task_create', TeacherTaskCreationView.as_view(), name='task_create_teacher'),
    path('<int:pk>/teacher/post_detail/<uuid:pk>', TeacherTaskCreationView.as_view(), name='post_detail_teacher'),
]
