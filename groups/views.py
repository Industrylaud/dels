from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from groups.models import Post, Comment


class GroupView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'groups/student_group.html'
    fields = ['body', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.filter(
            student_group=self.request.user.student_group
        ).order_by('-pub_date')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.student_group = self.request.user.student_group
        return super().form_valid(form)


class PostView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'groups/post_detail.html'
    fields = ['body', ]

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=int(self.kwargs['pk']))
        if post.student_group == self.request.user.student_group:
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, pk=int(self.kwargs['pk']))
        if post.student_group == self.request.user.student_group:
            context = super().get_context_data(**kwargs)
            context['post'] = Post.objects.get(id=int(self.kwargs['pk']))
            context['comments'] = self.model.objects.filter(post_id=int(self.kwargs['pk'])).order_by('-pub_date')
            return context
        return HttpResponseForbidden()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=int(self.kwargs['pk']))
        return super().form_valid(form)


