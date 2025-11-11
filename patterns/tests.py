from django.test import TestCase


class PatternsViewTests(TestCase):
    def test_patterns_page(self):
        response = self.client.get('/patterns/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_list.html')

    def test_pattern_detail_page(self):
        # Create a sample pattern to test detail view
        from patterns.models import Pattern
        pattern = Pattern.objects.create(title="Test Pattern", price=10.00)

        response = self.client.get(f'/patterns/{pattern.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_detail.html')

    def test_nonexistent_pattern_detail_page(self):
        response = self.client.get('/patterns/9999/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class PatternModelTests(TestCase):
    def test_pattern_creation(self):
        from patterns.models import Pattern
        pattern = Pattern.objects.create(title="New Pattern", price=15.00)
        self.assertEqual(pattern.title, "New Pattern")
        self.assertEqual(pattern.price, 15.00)

    def test_pattern_deletion(self):
        from patterns.models import Pattern
        pattern = Pattern.objects.create(title="To be deleted", price=20.00)
        pattern_id = pattern.id
        pattern.delete()
        with self.assertRaises(Pattern.DoesNotExist):
            Pattern.objects.get(id=pattern_id)

    def test_pattern_update(self):
        from patterns.models import Pattern
        pattern = Pattern.objects.create(title="Old Title", price=25.00)
        pattern.title = "Updated Title"
        pattern.save()
        updated_pattern = Pattern.objects.get(id=pattern.id)
        self.assertEqual(updated_pattern.title, "Updated Title")
