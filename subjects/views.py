from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView

from .forms import TaskCreationForm
from .models import PostInSubject, Task, Resource, Subject, CommentInSubject, CommentTask


class TeacherSubjectView(LoginRequiredMixin, ListView):
    template_name = 'subjects/teacher_subject.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))
        context = super().get_context_data(**kwargs)
        if get_object_or_404(subject.teachers, teacher=self.request.user):
            context['tasks'] = Task.objects.filter(subject_id=int(self.kwargs['pk'])).order_by('-pub_date')
            context['resources'] = Resource.objects.filter(subject_id=int(self.kwargs['pk'])).order_by('-pub_date')
            context['subject'] = subject
            return context
        return context

    def get_queryset(self):
        return PostInSubject.objects.filter(subject_id=int(self.kwargs['pk'])).order_by('-pub_date')


class TeacherPostCreationView(LoginRequiredMixin, CreateView):
    model = PostInSubject
    template_name = 'subjects/teacher_posts_creation.html'
    fields = [
        'body',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.subject = Subject.objects.get(id=int(self.kwargs['pk']))
        return super().form_valid(form)


class SubjectPostDetailView(LoginRequiredMixin, CreateView):
    model = CommentInSubject
    template_name = 'subjects/subject_post_detail.html'
    fields = [
        'body',
    ]

    def get(self, request, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))

        if get_object_or_404(subject.teachers, teacher=self.request.user) or \
                get_object_or_404(subject.students, user=self.request.user):
            return super().get(request, *args, **kwargs)

        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        post = get_object_or_404(PostInSubject, pk=int(self.kwargs['id']))
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))
        user = get_user_model()

        if get_object_or_404(subject.teachers, teacher=self.request.user) or \
                get_object_or_404(subject.students, user=self.request.user):
            context = super().get_context_data(**kwargs)
            context['post'] = post
            context['comments'] = self.model.objects.filter(post_id=int(self.kwargs['id'])).order_by('-pub_date')
            return context

        return HttpResponseForbidden()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = PostInSubject.objects.get(id=int(self.kwargs['pk']))
        return super().form_valid(form)


class TeacherTaskCreationView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = 'subjects/teacher_tasks_creation.html'

    def form_valid(self, form):
        form.instance.subject = Subject.objects.get(id=int(self.kwargs['pk']))
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, CreateView):
    model = CommentTask
    template_name = 'subjects/task_detail.html'
    fields = [
        'body',
    ]

    def get(self, request, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))

        if get_object_or_404(subject.teachers, teacher=self.request.user) or \
                get_object_or_404(subject.students, user=self.request.user):
            return super().get(request, *args, **kwargs)

        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        task = get_object_or_404(Task, pk=int(self.kwargs['id']))
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))
        user = get_user_model()

        if get_object_or_404(subject.teachers, teacher=self.request.user) or \
                get_object_or_404(subject.students, user=self.request.user):
            context = super().get_context_data(**kwargs)
            context['task'] = task
            context['comments'] = self.model.objects.filter(task_id=int(self.kwargs['id'])).order_by('-pub_date')
            return context

        return HttpResponseForbidden()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task = Task.objects.get(id=int(self.kwargs['pk']))
        return super().form_valid(form)
