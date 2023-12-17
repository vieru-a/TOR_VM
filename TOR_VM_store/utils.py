from .models import *

nav_menu = [
    {'url_name': 'store_main', 'title': 'Главная'},
    {'url_name': 'store_main', 'title': 'Обратная связь'},
    {'url_name': 'store_main', 'title': 'Корзина'},
    {'url_name': 'store_main', 'title': 'Войти'},
    {'url_name': 'store_main', 'title': 'Регистрация'},
]


class DataMixin:
    # paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.filter(type='category')

        user_menu = nav_menu.copy()
        if self.request.user.is_authenticated:
            user_menu[-2] = {'url_name': 'store_main', 'title': 'Выйти'}
            user_menu[-1] = {'url_name': 'store_main', 'title': self.request.user.username}

        context['nav_menu'] = user_menu
        context['categories'] = categories
        # if 'category_selected' not in context:
        #     context['category_selected'] = 0
        return context
