from users.tests.base import BaseTest


class LoginTest(BaseTest):
    def test_view_correctly(self):
        """Проверка доступа к странице"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_user(self):
        """Авторизация пользователя"""
        self.client.post(self.register_url, self.user_register)
        response = self.client.post(self.login_url, self.user_login)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.email, self.user_login['username'])
