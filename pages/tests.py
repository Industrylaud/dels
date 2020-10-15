from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView


class HomePageTest(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def testHomePageStatusCode(self):
        self.assertEqual(self.response.status_code, 200)

    def testHomePageTemplate(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def testHomePageUrlResolvesHomePageView(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
