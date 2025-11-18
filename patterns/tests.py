from django.test import TestCase
from patterns.models import Pattern, Favorite
from django.urls import reverse
from django.contrib.auth.models import User


class PatternsViewTests(TestCase):
    def test_patterns_page(self):
        response = self.client.get('/patterns/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_list.html')

    def test_pattern_detail_page(self):
        pattern = Pattern.objects.create(title="Test Pattern", price=10.00)

        response = self.client.get(f'/patterns/{pattern.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_detail.html')

    def test_nonexistent_pattern_detail_page(self):
        response = self.client.get('/patterns/9999/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_add_pattern_staff_user(self):
        staff_user = User.objects.create_user(
            username='staffuser', password='testpass', is_superuser=True
        )
        self.client.login(username='staffuser', password='testpass')

        url = reverse('pattern_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_form.html')

    def test_add_pattern_non_staff_user(self):
        normal_user = User.objects.create_user(
            username='normaluser', password='testpass', is_staff=False
        )
        self.client.login(username='normaluser', password='testpass')

        response = self.client.get('/patterns/add/')
        self.assertEqual(response.status_code, 302)

    def test_update_pattern_superuser(self):
        superuser = User.objects.create_user(
            username='superuser', password='testpass', is_superuser=True
        )
        self.client.login(username='superuser', password='testpass')

        pattern = Pattern.objects.create(title="Update Test", price=20.00)
        url = reverse('pattern_edit', args=[pattern.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_form.html')

    def test_delete_pattern_superuser(self):
        superuser = User.objects.create_user(
            username='superuser2', password='testpass', is_superuser=True
        )
        self.client.login(username='superuser2', password='testpass')

        pattern = Pattern.objects.create(title="Delete Test", price=30.00)
        url = reverse('pattern_delete', args=[pattern.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Pattern.objects.filter(id=pattern.id).exists())


class FavoritesLoginRequiredTests(TestCase):
    def setUp(self):
        self.url = reverse("my_favorites")

    def test_favorites_requires_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)


class FavoritesAddedTests(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.pattern = Pattern.objects.create(
            title="Fav Pattern",
            price=12.00,
        )
        self.url = reverse("toggle_favorite", args=[self.pattern.id])
        self.client.login(**self.user_credentials)

    def test_add_favorite(self):
        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        qs = Favorite.objects.filter(
            user=self.user,
            pattern=self.pattern,
        )
        self.assertTrue(qs.exists())

    def test_remove_favorite(self):
        Favorite.objects.create(
            user=self.user,
            pattern=self.pattern,
        )
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        qs = Favorite.objects.filter(
            user=self.user,
            pattern=self.pattern,
        )
        self.assertFalse(qs.exists())


class PatternModelTests(TestCase):
    def test_pattern_creation(self):
        pattern = Pattern.objects.create(title="Test Pattern", price=15.00)
        self.assertEqual(pattern.title, "Test Pattern")
        self.assertEqual(pattern.price, 15.00)

    def test_pattern_deletion(self):
        pattern = Pattern.objects.create(title="To be deleted", price=20.00)
        pattern_id = pattern.id
        pattern.delete()
        with self.assertRaises(Pattern.DoesNotExist):
            Pattern.objects.get(id=pattern_id)

    def test_pattern_update(self):
        pattern = Pattern.objects.create(title="Old Title", price=25.00)
        pattern.title = "Updated Title"
        pattern.save()
        updated_pattern = Pattern.objects.get(id=pattern.id)
        self.assertEqual(updated_pattern.title, "Updated Title")
