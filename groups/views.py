from django.views.generic import ListView
from django.views.generic.edit import CreateView

from groups.models import Post
from users.models import StudentGroup


class GroupView(CreateView):
    model = Post
    template_name = 'groups/student_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.model.objects.all()
        return context
