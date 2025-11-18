from django.test import TestCase
from django.urls import reverse
from patterns.models import Pattern
from django.contrib.auth import get_user_model
from accounts.models import Profile
from checkout.models import Order


class CheckoutViewTests(TestCase):

    def test_checkout_page_renders_with_bag(self):
        p = Pattern.objects.create(title="Test", price=1.00)
        session = self.client.session
        session['bag'] = {str(p.id): 1}
        session.save()

        resp = self.client.get(reverse("checkout"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "checkout/checkout.html")

    def test_checkout_success_page_renders(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        profile, _ = Profile.objects.get_or_create(user=user)

        order = Order.objects.create(
            user_profile=profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='GB',
            town_or_city='Testville',
            street_address1='123 Test St',
        )

        self.client.login(username='testuser', password='testpass')

        url = reverse('checkout_success', args=[order.order_number])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "checkout/checkout_success.html")
