from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import StudentGroup


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


class StudentGroupTest(TestCase):

    def setUp(self):
        StudentGroup.objects.create(name='test group123')

    def testName(self):
        group = StudentGroup.objects.get(id=1)
        expected_group_name = f'{group}'
        self.assertEqual(expected_group_name, 'test group123')
