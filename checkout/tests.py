from django.test import TestCase
from django.urls import reverse
from patterns.models import Pattern


class CheckoutViewTests(TestCase):
    def test_checkout_page_renders_with_bag(self):
        # create a product and add to session bag
        p = Pattern.objects.create(title="Test", price=1.00)
        session = self.client.session
        session['bag'] = {str(p.id): 1}
        session.save()

        resp = self.client.get(reverse("checkout"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "checkout/checkout.html")
