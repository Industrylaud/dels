from django.urls import path

from subjects.views import *

urlpatterns = [
    path('<int:pk>/teacher', TeacherSubjectView.as_view(), name='teacher_subject'),
    path('<int:pk>/teacher/post_create', TeacherPostCreationView.as_view(), name='post_create_teacher'),
    path('<int:pk>/teacher/task_create', TeacherTaskCreationView.as_view(), name='task_create_teacher'),
    path('<int:pk>/teacher/post_detail/<int:id>', SubjectTeacherPostDetailView.as_view(), name='post_detail_subject'),
    path('<int:pk>/post_detail/<int:id>', SubjectStudentPostDetailView.as_view(), name='post_detail_subject'),
    path('<int:pk>/teacher/task_detail/<uuid:id>', TeacherTaskDetailView.as_view(), name='task_detail_subject'),
    path('<int:pk>/task_detail/<uuid:id>', TeacherTaskDetailView.as_view(), name='task_detail_subject'),
    path('<int:pk>/teacher/tasks_done/<uuid:id>', TasksDoneListView.as_view(), name='task_done_list'),
    path('teacher/task_done/<uuid:id>', TaskDoneTeacherEditView.as_view(), name='task_done_teacher_edit'),
    path('<int:pk>/teacher/resource_create', TeacherResourceCreateView.as_view(), name='resource_create'),
    path('<int:pk>/teacher/resource_delete/<uuid:id>', TeacherResourceDeleteView.as_view(), name='resource_delete'),
    path('teacher/create_subject', TeacherCreateSubjectView.as_view(), name='subject_create_teacher'),
    path('<int:pk>/teacher/add_students', TeacherAddStudentsView.as_view(), name='teacher_add_students'),
    path('<int:pk>', StudentSubjectView.as_view(), name='student_subject'),
]
