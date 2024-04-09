from django.contrib.auth import get_user_model

from users.tests.base import BaseTest


class ChangeProfileTest(BaseTest):
    def test_view_correctly(self):
        """Проверка доступа к странице"""
        response = self.client.get(self.profile_change_url)
        self.assertEqual(response.status_code, 302)
        # Редирект неавторизованного пользователя
        self.assertEqual(response.url, '/accounts/login/?next=/users/profile/')

    def test_change_profile(self):
        """Изменение данных пользователя в профиле"""
        # регистрация пользователя
        self.client.post(self.register_url, self.user_register, format='text/html')
        # авторизация пользователя
        self.client.post(self.login_url, self.user_login)
        self.assertTemplateUsed(self.client.get(self.profile_change_url), 'users/profile.html')
        self.user_register['first_name'] = 'Новое имя'
        # изменение имени пользователя
        response = self.client.post(self.profile_change_url, self.user_register)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/profile/')
        self.assertEqual(get_user_model().objects.first().first_name, 'Новое имя')
