from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import PostInSubject, Task, Resource, Subject


class TeacherSubjectView(LoginRequiredMixin, ListView):
    template_name = 'subjects/teacher_subject.html'

    def get_context_data(self, **kwargs):
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))
        if subject.teachers.get(teacher=self.request.user):
            context = super().get_context_data(**kwargs)
            context['tasks'] = Task.objects.filter(subject_id=int(self.kwargs['pk'])).order_by('-pub_date')
            context['resources'] = Resource.objects.filter(subject_id=int(self.kwargs['pk'])).order_by('-pub_date')
            context['subject'] = subject
            return context
        return HttpResponseForbidden()

    def get_queryset(self):
        return PostInSubject.objects.filter(subject_id=int(self.kwargs['pk'])).order_by('-pub_date')