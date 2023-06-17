from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView


# Create your tests here.
class TestHomePage(TestCase):
    def setUp(self) -> None:
        url = reverse("home")
        self.response = self.client.get(url)

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


class TestHomePage(TestCase):
    def setUp(self) -> None:
        url = reverse("application")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "application.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Applications")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Not supposed to be here")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("application/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
