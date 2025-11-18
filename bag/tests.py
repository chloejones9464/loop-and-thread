from django.test import TestCase
from django.urls import reverse
from patterns.models import Pattern


class BagViewTests(TestCase):

    def test_bag_page_renders(self):
        response = self.client.get(reverse("view_bag"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bag/bag.html")

    def test_add_to_bag_adds_item(self):
        pattern = Pattern.objects.create(title="Test Pattern")

        response = self.client.post(
            reverse("add_to_bag", args=[pattern.id]),
            data={"redirect_url": "/"}
        )
        self.assertRedirects(response, "/")
        session_bag = self.client.session.get("bag", {})
        self.assertIn(str(pattern.id), session_bag)

    def test_remove_from_bag_removes_item(self):
        pattern = Pattern.objects.create(title="Test Pattern")
        session = self.client.session
        session["bag"] = {str(pattern.id): True}
        session.save()

        response = self.client.post(
            reverse("remove_from_bag", args=[pattern.id]),
            data={"redirect_url": "/"}
        )
        self.assertRedirects(response, "/")
        session_bag = self.client.session.get("bag", {})
        self.assertNotIn(str(pattern.id), session_bag)
