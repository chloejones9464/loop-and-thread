from django.test import TestCase
from django.urls import reverse


class BagViewTests(TestCase):

    def test_bag_page_renders(self):
        response = self.client.get(reverse("view_bag"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bag/bag.html")
