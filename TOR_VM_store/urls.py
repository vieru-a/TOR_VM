from django.urls import path, include
from .views import ProductsList, CategoryDetail, ProductDetail


urlpatterns = [
    path('', ProductsList.as_view(), name='store_main'),
    path('category/<slug:category_slug>/', CategoryDetail.as_view(), name='store_category_detail'),
    path('product/<str:product_slug>/', ProductDetail.as_view(), name='store_product_detail'),
]
