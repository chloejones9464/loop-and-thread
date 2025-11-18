from django.test import TestCase
from .models import NewsPost
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class NewsViewTests(TestCase):
    def test_news_page(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_news_detail_page(self):
        # create a sample news post for testing
        post = NewsPost.objects.create(
            title="Test Post",
            summary="This is a test summary.",
            body="This is the body of the test post.",
            status=NewsPost.PUBLISHED,
        )
        response = self.client.get(f'/news/{post.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')

    def test_news_create_page_requires_login(self):
        url = reverse("news_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_news_add_page_allows_staff_user(self):
        staff = User.objects.create_user(
            username="staff",
            email="staff@test.com",
            password="pass123",
            is_staff=True,
        )

        logged_in = self.client.login(username="staff", password="pass123")
        self.assertTrue(logged_in)

        url = reverse("news_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_form.html")

    def test_update_news_page_requires_staff_user(self):
        # create a sample news post for testing
        post = NewsPost.objects.create(
            title="Test Post",
            summary="This is a test summary.",
            body="This is the body of the test post.",
            status=NewsPost.PUBLISHED,
        )

        url = reverse("news_edit", kwargs={"slug": post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_news_edit_page_allows_staff_user(self):
        staff = User.objects.create_user(
            username="staff",
            email="staff@test.com",
            password="pass123",
            is_staff=True,
        )
        logged_in = self.client.login(username="staff", password="pass123")
        self.assertTrue(logged_in)

        post = NewsPost.objects.create(
            title="Old Title",
            summary="Old summary.",
            body="Old body.",
            status=NewsPost.PUBLISHED,
        )

        url = reverse("news_edit", kwargs={"slug": post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_form.html")

    def test_news_delete_page_requires_staff_user(self):
        # create a sample news post for testing
        post = NewsPost.objects.create(
            title="Test Post",
            summary="This is a test summary.",
            body="This is the body of the test post.",
            status=NewsPost.PUBLISHED,
        )

        url = reverse("news_delete", kwargs={"slug": post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)
