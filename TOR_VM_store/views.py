from django.views.generic import ListView, DetailView

from .models import Product, Category

nav_menu = ['Главная страница', 'Обратная связь', 'Корзина', 'Войти', 'Зарегистрироваться']


class ProductsList(ListView):
    model = Product
    template_name = 'TOR_VM_store/store_main.html'
    context_object_name = 'data'
    extra_context = {'nav_selected': 0}

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context()
        # return {**context, **c_def}

    def get_queryset(self):
        return Product.objects.all()[0:9]


class CategoryDetail(DetailView):
    model = Category
    template_name = 'TOR_VM_store/store_category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.product_set.all()
        return context
        # c_def = self.get_user_context()
        # return {**context, **c_def}


class ProductDetail(DetailView):
    model = Product
    template_name = 'TOR_VM_store/store_product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context()
    #     return {**context, **c_def}
