from django.contrib.auth import get_user_model

from users.tests.base import BaseTest


class PasswordChangeTest(BaseTest):
    def test_view_correctly(self):
        """Проверка доступа к странице"""
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 302)
        # Редирект неавторизованного пользователя
        self.assertEqual(response.url, '/accounts/login/?next=/users/password_change/')

    def test_password_change(self):
        """Смена пароля"""
        # регистрация пользователя
        self.client.post(self.register_url, self.user_register)
        # авторизация пользователя
        self.client.post(self.login_url, self.user_login)
        self.assertTemplateUsed(self.client.get(self.password_change_url), 'users/password_change_form.html')
        old_password = get_user_model().objects.first().password
        # изменение пароля
        self.client.post(self.password_change_url, self.user_new_password)
        self.assertNotEqual(get_user_model().objects.first().password, old_password)
        # выход из аккаунта
        self.client.logout()
        # авторизация с новым паролем
        response = self.client.post(self.login_url, {'username': self.user_login['username'],
                                                     'password': self.user_new_password['new_password1']})
        self.assertEqual(response.url, '/')
        self.assertEqual(response.wsgi_request.user.email, self.user_login['username'])
