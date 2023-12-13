from django.urls import path
from .views import MainPage, ProductsListAPIView

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('api/v1/productslist/', ProductsListAPIView.as_view())
]
