from django.contrib.auth import get_user_model
from django.test import TestCase


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

    def test_create_superuser(self):
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