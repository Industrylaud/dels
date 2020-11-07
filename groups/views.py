from django.views.generic import ListView

from groups.models import Post
from users.models import StudentGroup


class GroupView(ListView):
    model = Post
    template_name = 'groups/student_group.html'
