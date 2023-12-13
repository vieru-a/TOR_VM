from django.views.generic import ListView
from rest_framework import generics

from .models import Product
from .serializers import ProductsSerializer


class MainPage(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'data'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Интернет-магазин ТОР-ВМ'
        return context

    def get_queryset(self):
        return Product.objects.all()[:10]


class ProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
