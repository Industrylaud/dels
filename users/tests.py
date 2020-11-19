from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from .models import StudentGroup
from .views import UserProfileView


class CustomUserTests(TestCase):

    def testCreateUser(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            first_name='testename',
            last_name='testlast',
            password='password123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@email.com')
        self.assertEqual(user.first_name, 'testename')
        self.assertEqual(user.last_name, 'testlast')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def testCreateSuperuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@email.com',
            password='password123'
        )
        self.assertEqual(admin_user.username, 'testadmin')
        self.assertEqual(admin_user.email, 'testadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class StudentGroupTests(TestCase):

    def setUp(self):
        StudentGroup.objects.create(name='testgroup')

    def testName(self):
        expected_group_name = StudentGroup.objects.all()[0].name
        self.assertEqual(expected_group_name, 'testgroup')


class SignupTests(TestCase):

    username = 'testuser'
    email = 'testuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def testSignupTemplate(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')

    def testSignupForm(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username,
                         self.username)
        self.assertEqual(get_user_model().objects.all()[0].email,
                         self.email)


class UserProfileTests(TestCase):

    username = 'testuser'
    email = 'test@email.pl'
    first_name = 'johnny'
    last_name = 'test'
    password = 'testpass123'

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
        )
        self.url = reverse('user_profile')

    def testUserProfileStatusCode(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def testUserProfileTemplate(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'user_profile.html')

    def testUserProfileUrlResolveUserProfileView(self):
        view = resolve('/accounts/profile/')
        self.assertEqual(view.func.__name__, UserProfileView.as_view().__name__)

    def testUserProfileContainsCorrectHtml(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertContains(response, self.username)
        self.assertContains(response, self.email)
        self.assertContains(response, self.first_name)
        self.assertContains(response, self.last_name)
