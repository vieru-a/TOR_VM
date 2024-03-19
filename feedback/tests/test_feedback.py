from django.test import TestCase
from django.urls import reverse_lazy


class FeedbackTest(TestCase):
    def setUp(self):
        self.page = reverse_lazy('feedback:feedback_page')
        self.data = {'first_name': 'Имя',
                     'last_name': 'Фамилия',
                     'email': 'test@testmail.ru',
                     'message': 'Перезвоните мне, пожалуйста. Мой номер телефона: 89011011121'}
        return super().setUp()

    def test_feedback(self):
        response = self.client.post(self.page, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/feedback/success/')
        self.assertTemplateUsed(self.client.get(self.page), 'feedback/feedback_page.html')
