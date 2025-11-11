from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from patterns.models import Pattern
from accounts.models import Profile

User = get_user_model()


class ReviewMinimalViewTests(TestCase):
    def setUp(self):
        # Minimal data needed for the view: a pattern and a user
        self.pattern = Pattern.objects.create(title="Cozy Pumpkin", price=4.99)
        self.create_url = reverse("create_review", args=[self.pattern.id])
        self.detail_url = reverse("pattern_detail", args=[self.pattern.id])

        self.user = User.objects.create_user(
            username="chloe", email="chloe@test.com", password="pass12345"
        )
        Profile.objects.get_or_create(user=self.user)

    def test_anonymous_is_redirected_to_login(self):
        resp = self.client.post(
            self.create_url,
            data={"rating": 5, "comment": "Nice"},
        )
        self.assertEqual(resp.status_code, 302)

    def test_logged_in_non_buyer_gets_redirected_back(self):
        self.client.login(username="chloe", password="pass12345")
        resp = self.client.post(
            self.create_url,
            data={"rating": 5, "comment": "Nice"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.view_name, "pattern_detail")
