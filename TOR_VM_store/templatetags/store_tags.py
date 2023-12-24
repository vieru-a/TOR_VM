from django import template
from TOR_VM_store.models import Category


register = template.Library()


@register.inclusion_tag('TOR_VM_store/includes/nav_menu.html')
def get_nav_menu(user, nav_selected=0):
    nav_menu = [
        {'id': 0, 'url_name': 'store_main', 'title': 'Главная'},
        {'id': 1, 'url_name': 'store_main', 'title': 'Обратная связь'},
        {'id': 2, 'url_name': 'store_main', 'title': 'Корзина'},
    ]
    reg = {'id': 3, 'title': 'Регистрация'}
    login = {'id': 4, 'title': 'Войти'}
    logout = {'id': 4, 'title': 'Выйти'}
    return {'nav_menu': nav_menu,
            'user': user,
            'reg': reg,
            'login': login,
            'logout': logout,
            'nav_selected': nav_selected,
            }


@register.inclusion_tag('TOR_VM_store/includes/categories.html')
def get_categories():
    category = Category.objects.filter(type='category')
    return {'menu_category': category}

