from django import template
from TOR_VM_store.models import Category


register = template.Library()


@register.inclusion_tag('TOR_VM_store/includes/nav_menu.html')
def get_nav_menu(user):
    nav_menu = [
        {'url_name': 'store_main', 'title': 'Главная'},
        {'url_name': 'store_main', 'title': 'Обратная связь'},
        {'url_name': 'store_main', 'title': 'Корзина'},
    ]
    return {'nav_menu': nav_menu, 'user': user}


@register.inclusion_tag('TOR_VM_store/includes/categories.html')
def get_categories():
    category = Category.objects.filter(type='category')
    return {'menu_category': category}

