from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView

from users.models import StudentGroup
from .forms import TaskCreationForm, ResourceCreationForm, StudentGroupAddForm
from .models import PostInSubject, Task, Resource, Subject, CommentInSubject, CommentTask, TaskDone, Teacher


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

        if get_object_or_404(subject.teachers, teacher=self.request.user) or \
                get_object_or_404(subject.students, user=self.request.user):
            context = super().get_context_data(**kwargs)
            context['post'] = post
            context['comments'] = self.model.objects.filter(post_id=int(self.kwargs['id'])).order_by('-pub_date')
            return context

        return HttpResponseForbidden()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = PostInSubject.objects.get(id=int(self.kwargs['id']))
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
        task = get_object_or_404(Task, pk=self.kwargs['id'])
        subject = get_object_or_404(Subject, pk=int(self.kwargs['pk']))

        if get_object_or_404(subject.teachers, teacher=self.request.user) or \
                get_object_or_404(subject.students, user=self.request.user):
            context = super().get_context_data(**kwargs)
            context['task'] = task
            context['comments'] = self.model.objects.filter(task_id=self.kwargs['id']).order_by('-pub_date')
            return context

        return HttpResponseForbidden()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task = Task.objects.get(id=self.kwargs['id'])
        return super().form_valid(form)


class TeacherResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    template_name = 'subjects/teacher_resource_creation.html'
    form_class = ResourceCreationForm

    def form_valid(self, form):
        form.instance.subject = Subject.objects.get(id=int(self.kwargs['pk']))
        return super().form_valid(form)


class TeacherResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = 'subjects/teacher_resource_delete.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        subject = self.object.subject
        return reverse_lazy('teacher_subject', args=[str(subject.id)])


class TasksDoneListView(LoginRequiredMixin, ListView):
    model = TaskDone
    template_name = 'subjects/teacher_tasks_done.html'
    user = get_user_model()
    context_object_name = 'tasks_done'

    def get_queryset(self):
        return TaskDone.objects.filter(task_id=self.kwargs['id']).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(pk=int(self.kwargs['pk']))
        context['students'] = subject.students.all()
        return context


class TaskDoneTeacherEditView(LoginRequiredMixin, UpdateView):
    model = TaskDone
    template_name = 'subjects/teacher_task_done_.html'
    fields = [
        'grade',
        'feedback',
        'status'
    ]
    context_object_name = 'done'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_done'] = self.model.objects.get(id=self.kwargs['id'])
        return context


class TeacherCreateSubjectView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = ['subject_name']
    template_name = 'subjects/teacher_subject_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.instance.teachers.add(Teacher.objects.get(teacher_id=self.request.user.id))
        return super().form_valid(form)


class TeacherAddStudentsView(LoginRequiredMixin, FormView):
    form_class = StudentGroupAddForm
    template_name = 'subjects/teacher_add_students.html'

    def get_success_url(self):
        subject = Subject.objects.get(pk=int(self.kwargs['pk']))
        return reverse_lazy('teacher_subject', args=[str(subject.id)])

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid() and StudentGroup.objects.filter(name=form.data['group']).exists():
            group = StudentGroup.objects.get(name=form.data['group'])
            user = get_user_model()
            subject = Subject.objects.get(pk=int(self.kwargs['pk']))
            for student in user.objects.filter(student_group_id=group.id):
                subject.students.add(student.id)
                subject.save()

            return HttpResponseRedirect(reverse('teacher_subject', args=[str(subject.id)]))

        return render(request, self.template_name, {'form': form, 'error_message': "wrong group"})
