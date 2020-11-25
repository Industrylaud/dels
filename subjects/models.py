from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models


class Teacher(models.Model):
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return get_user_model().username


class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.subject_name


class PostInSubject(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    body = models.TextField()
    pub_date = models.DateTimeField('date_published', auto_now_add=True)

    def __str__(self):
        return self.body


class CommentInSubject(models.Model):
    post = models.ForeignKey(
        PostInSubject,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    body = models.TextField(max_length=4000)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)

    def __str__(self):
        return self.body


class Task(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    deadline = models.DateTimeField('date to end')
    body = models.TextField()
    file = models.FileField(upload_to=f"tasks/{id}/", null=True, blank=True)


class CommentTask(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    body = models.TextField(max_length=4000)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)

    def __str__(self):
        return self.body


class TaskDone(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='tasks_done',
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    message = models.TextField(max_length=4000, null=True, blank=True)
    feedback = models.TextField(max_length=4000, null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to=f"done_tasks/{id}/", null=True, blank=True)

    NotDone = 1
    Done = 2
    ToEdit = 3

    STATUS = (
        (NotDone, _('Not done')),
        (Done, _('Done')),
        (ToEdit, _('To edit')),
    )

    status = models.SmallIntegerField(
        choices=STATUS,
        default=1,
    )
