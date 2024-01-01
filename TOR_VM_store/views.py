from django.views.generic import ListView, DetailView

from .models import Product, Category


class ProductsList(ListView):
    model = Product
    template_name = 'TOR_VM_store/store_main.html'
    context_object_name = 'data'
    extra_context = {'nav_selected': 0}

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
        context['cat_selected'] = self.object.id
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'TOR_VM_store/store_product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

