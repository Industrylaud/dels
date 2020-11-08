from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from groups.models import Post


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
