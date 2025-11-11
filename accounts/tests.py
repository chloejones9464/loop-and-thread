from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='chloe', email='chloe@test.com', password='pass12345'
        )

    def test_accounts_home_authenticated(self):
        self.client.login(username='chloe', password='pass12345')
        resp = self.client.get('/accounts/')
        self.assertIn(resp.status_code, (200, 302))

    def test_accounts_unauthenticated_user(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 302)
