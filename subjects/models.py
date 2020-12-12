import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def dir_name(instance, filename):
    idd = (str(instance.id))
    return f"{idd}/{filename}"


class Teacher(models.Model):
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.teacher.username


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
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

    def get_absolute_url(self):
        return reverse('teacher_subject', args=[str(self.subject_id)])


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

    def get_absolute_url(self):
        return reverse('post_detail_subject', args=[
            str(self.post.subject_id),
            str(self.post_id)
        ])


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    deadline = models.DateField('date to end')
    body = models.TextField()

    file = models.FileField(upload_to=f"tasks/to_do/", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('teacher_subject', args=[str(self.subject_id)])


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
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

    @property
    def dir_name(self):
        return f"{self.task.subject.id}/{self.task.id}/{self.author.username}/"

    file = models.FileField(
        upload_to=f"done_tasks/{dir_name}", null=True, blank=True
    )

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


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='resources',
    )
    name = models.CharField(max_length=255)
    body = models.TextField(max_length=4000)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)

    @property
    def dir_name(self):
        return f"{self.subject.id}/{self.id}/"

    file = models.FileField(upload_to=f"resources/{dir_name}", null=True, blank=True)
