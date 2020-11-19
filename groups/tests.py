from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from groups.models import Post, Comment
from groups.views import GroupView
from users.models import StudentGroup


class GroupPageTests(TestCase):
    username = 'testuser'
    email = 'test@email.pl'
    first_name = 'johnny'
    last_name = 'test'
    password = 'testpass123'

    group_name = 'testgroup'
    post_body = 'sample test post body'
    comment_body = 'sample comment body'


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
        self.post = Post.objects.create(
            body=self.post_body,
            author_id=self.user.id,
            student_group_id=self.user.student_group.id
        )
        self.comment = Comment.objects.create(body=self.comment_body, author_id=self.user.id, post_id=self.post.id)

    def testStudentGroupPageStatusCode(self):
        self.assertEqual(self.response.status_code, 200)

    def testStudentGroupPageTemplate(self):
        self.assertTemplateUsed(self.response, 'groups/student_group.html')

    def testStudentGroupPageResolveStudentGroupView(self):
        view = resolve('/groups/mygroup/')
        self.assertEqual(view.func.__name__, GroupView.as_view().__name__)

    def testAddPost(self):
        self.assertEqual(Post.objects.all()[0].body, self.post_body)
        self.assertEqual(Post.objects.all().count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertContains(response, self.post_body)
        self.assertContains(response, self.user.username)

    def testAddComment(self):
        self.assertEqual(Comment.objects.all()[0].body, self.comment_body)
        self.assertEqual(Comment.objects.all().count(), 1)
        url = reverse('post_detail', args='1')
        response = self.client.get(url, follow=True)
        self.assertContains(response, self.comment_body)
        self.assertTemplateUsed(response, 'groups/post_detail.html')
        self.assertEqual(response.status_code, 200)
