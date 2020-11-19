from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from users.models import StudentGroup


class Post(models.Model):
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    body = models.TextField()
    pub_date = models.DateTimeField('date_published', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('student_group')


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
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
        return reverse('post_detail', args=[str(self.post_id)])
