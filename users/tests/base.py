from django.test import TestCase
from django.urls import reverse_lazy


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse_lazy('users:register')
        self.login_url = reverse_lazy('users:login')
        self.profile_change_url = reverse_lazy('users:profile')
        self.password_change_url = reverse_lazy('users:password_change')

        self.user_register = {'email': 'test@testmail.ru',
                              'phone_number': '89011011121',
                              'first_name': 'Имя',
                              'last_name': 'Фамилия',
                              'business_type': 'individuals',
                              'address1': 'Осенний проспект',
                              'city': 'Moscow',
                              'country': 'RU',
                              'mailing': False,
                              'password1': 'OldPassword123',
                              'password2': 'OldPassword123'}

        self.user_login = {'username': self.user_register['email'],
                           'password': self.user_register['password1']}

        self.user_new_password = {'old_password': 'OldPassword123',
                                  'new_password1': 'NewPassword123',
                                  'new_password2': 'NewPassword123'}
        return super().setUp()
