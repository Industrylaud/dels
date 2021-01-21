from django.db import models

from subjects.models import Subject


class SubjectEvent(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    date = models.DateField('event date')
    name = models.CharField(max_length=255)
    body = models.TextField()


def add_event(subject_id, date, name, body):
    subject_event = SubjectEvent(
        subject_id=subject_id,
        date=date,
        name=name,
        body=body
    )
    subject_event.save()
