from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .views import *


# Create your tests here.
class TestHomePage(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="test",
            email="test@django.com",
            password="testpass123",
        )
        self.client = Client()
        self.client.login(username="test", password="testpass123")
        self.response = self.client.get(reverse("home"))

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Home Page")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Not supposed to be here")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
