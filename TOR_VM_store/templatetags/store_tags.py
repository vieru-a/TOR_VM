from django import template
from TOR_VM_store.models import Category


register = template.Library()


@register.inclusion_tag('TOR_VM_store/includes/nav_menu.html', takes_context=True)
def get_nav_menu(context, user, nav_selected=0):
    nav_menu = [
        {'id': 0, 'url_name': 'store_main', 'title': 'Главная'},
        {'id': 1, 'url_name': 'feedback:feedback_page', 'title': 'Обратная связь'},
        {'id': 2, 'url_name': 'cart:cart_detail', 'title': 'Корзина'},
        {'id': 3, 'url_name': 'users:register', 'title': 'Регистрация'},
        {'id': 4, 'url_name': 'users:login', 'title': 'Войти'},
    ]

    if user.is_authenticated:
        nav_menu[3] = {'id': 3, 'url_name': 'users:profile', 'title': f'{user.email}'}
        nav_menu.pop(4)

    if context['cart'].get_total_price() > 1:
        nav_menu[2] = {'id': 2, 'url_name': 'cart:cart_detail',
                       'title': f'Корзина: {context["cart"].get_total_price()} руб.'}

    return {'nav_menu': nav_menu,
            'cart': context['cart'],
            'user': user,
            'nav_selected': nav_selected,
            }


@register.inclusion_tag('TOR_VM_store/includes/categories.html')
def get_categories(cat_selected):
    category = Category.objects.filter(type='category')
    return {'menu_category': category, 'cat_selected': cat_selected}
