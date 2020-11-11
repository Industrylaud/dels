from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from groups.views import GroupView
from users.models import StudentGroup


class GroupPageTests(TestCase):
    username = 'testuser'
    email = 'test@email.pl'
    first_name = 'johnny'
    last_name = 'test'
    password = 'testpass123'

    group_name = 'testgroup'

    def setUp(self):
        User = get_user_model()
        self.group = StudentGroup.objects.create(
            name=self.group_name
        )
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            student_group=self.group,
        )
        self.url = reverse('student_group')
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url, follow=True)

    def testStudentGroupPageStatusCode(self):
        self.assertEqual(self.response.status_code, 200)

    def testStudentGroupPageTemplate(self):
        self.assertTemplateUsed(self.response, 'groups/student_group.html')

    def testStudentGroupPageResolveStudentGroupView(self):
        view = resolve('/groups/mygroup/')
        self.assertEqual(view.func.__name__, GroupView.as_view().__name__)