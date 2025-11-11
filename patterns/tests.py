from django.test import TestCase


class PatternsViewTests(TestCase):
    def test_patterns_page(self):
        response = self.client.get('/patterns/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patterns/pattern_list.html')
