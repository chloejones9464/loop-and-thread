from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from patterns.models import Pattern
from checkout.models import Order, OrderLineItem
from reviews.models import Review
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

    def test_edit_review_logged_in_buyer(self):
        user = User.objects.create_user(
            username="buyer",
            email="buyer@test.com",
            password="testpass",
        )
        profile, _ = Profile.objects.get_or_create(user=user)

        pattern = Pattern.objects.create(
            title="Test Pattern",
            price=5.00,
        )

        order = Order.objects.create(
            user_profile=profile,
            full_name="Test Buyer",
            email="buyer@test.com",
            phone_number="1234567890",
            country="GB",
            town_or_city="Testville",
            street_address1="123 Test St",
        )
        OrderLineItem.objects.create(
            order=order,
            pattern=pattern,
        )

        review = Review.objects.create(
            pattern=pattern,
            user_profile=profile,
            rating=5,
            body="Great pattern!",
        )

        self.client.login(username="buyer", password="testpass")

        url = reverse("edit_review", kwargs={"review_id": review.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_form.html")

    def test_delete_review_logged_in_buyer(self):
        user = User.objects.create_user(
            username="buyer",
            email="buyer@test.com",
            password="testpass",
        )
        profile, _ = Profile.objects.get_or_create(user=user)

        pattern = Pattern.objects.create(
            title="Test Pattern",
            price=5.00,
        )

        order = Order.objects.create(
            user_profile=profile,
            full_name="Test Buyer",
            email="buyer@test.com",
            phone_number="1234567890",
            country="GB",
            town_or_city="Testville",
            street_address1="123 Test St",
        )
        OrderLineItem.objects.create(
            order=order,
            pattern=pattern,
        )

        review = Review.objects.create(
            pattern=pattern,
            user_profile=profile,
            rating=5,
            body="Great pattern!",
        )

        self.client.login(username="buyer", password="testpass")

        url = reverse("delete_review", kwargs={"review_id": review.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_logged_in_non_buyer_gets_redirected_back(self):
        self.client.login(username="chloe", password="pass12345")
        resp = self.client.post(
            self.create_url,
            data={"rating": 5, "comment": "Nice"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.view_name, "pattern_detail")
