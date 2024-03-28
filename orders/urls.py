from django.urls import path, include

from orders.views import OrderCreate

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
]
