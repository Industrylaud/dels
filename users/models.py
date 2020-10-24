from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class StudentGroup(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=255
    )

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    index_number = models.CharField(
        max_length=7,
        unique=True,
        null=True,
        blank=True
    )
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    A, B, C, D, E = 1, 2, 3, 4, 5
    SUB_GROUP = (
        (A, _('A')),
        (B, _('B')),
        (C, _('C')),
        (D, _('D')),
        (E, _('E')),
    )
    sub_group = models.PositiveSmallIntegerField(
        choices=SUB_GROUP,
        default=1,
        null=True,
        blank=True
    )
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]
    first_name = models.CharField(max_length=255, blank=False, null=True)
    last_name = models.CharField(max_length=255, blank=False, null=True)

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.username)])




