from django.contrib.auth import get_user_model
from django.db import models

from users.models import StudentGroup


class Post(models.Model):
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    body = models.TextField()
    pub_date = models.DateTimeField('date_published')


