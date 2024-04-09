from django.contrib.auth import get_user_model

from users.tests.base import BaseTest


class RegisterTest(BaseTest):

    def test_view_correctly(self):
        """Проверка доступа к странице"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user(self):
        """Регистрация пользователя (Физическое лицо)"""
        response = self.client.post(self.register_url, self.user_register)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login/')
        self.assertEqual(get_user_model().objects.first().email, self.user_register['email'])

    def test_register_individuals_user(self):
        """Регистрация пользователя (Физическое лицо) с необязательными полями"""
        self.user_register['fax'] = '70953333333'
        self.user_register['company'] = 'Warmane'
        self.user_register['address2'] = 'Зимняя улица'
        self.user_register['index'] = '117542'
        response = self.client.post(self.register_url, self.user_register)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login/')
        self.assertEqual(get_user_model().objects.first().fax, '70953333333')

    def test_register_legal_entities_user(self):
        """Регистрация пользователя (Юридическое лицо)"""
        self.user_register['business_type'] = 'legal_entities'
        self.user_register['legal_name'] = 'Тестовая организация'
        self.user_register['inn'] = '123456789012'
        self.user_register['kpp'] = '561001001'
        self.user_register['legal_address'] = 'г. Москва'
        self.user_register['file_with_contacts'] = r'C:\Users\drear\Downloads\datatype.pdf'
        response = self.client.post(self.register_url, self.user_register)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login/')
        self.assertEqual(get_user_model().objects.first().business_type, 'legal_entities')
