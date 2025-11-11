from django.test import TestCase


class NewsViewTests(TestCase):
    def test_news_page(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')
