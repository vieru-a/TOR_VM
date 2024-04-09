from django.test import TestCase

from django.urls import reverse_lazy

from TOR_VM_store.models import Category, Product
from orders.models import Order


class OrdersTest(TestCase):
    def setUp(self):
        self.cart_url = reverse_lazy('cart:cart_add', kwargs={'product_id': 1})
        self.order_url = reverse_lazy('orders:order_create')
        self.product = {'name': 'Валикодержатель',
                        'slug': '1_010',
                        'image': 'products/Валикодержатели/Валикодержатель/1.010.jpg',
                        'article_number': '1.010',
                        'price': '209.00',
                        'description': 'test',
                        'is_available': True}
        self.category = {'name': 'Валикодержатели',
                         'image': 'products/Валикодержатели/Валикодержатели.jpg',
                         'description': 'test',
                         'type': 'category'}
        self.order = {'first_name': 'Имя',
                      'last_name': 'Фамилия',
                      'phone_number': '89011011121',
                      'email': 'test@testmail.ru',
                      'address1': 'Осенний проспект',
                      'city': 'Moscow',
                      'country': 'RU'}

        return super().setUp()

    def test_view_correctly(self):
        """Проверка доступа к странице"""
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create.html')

    def test_orders(self):
        """Проверка создания заказа"""
        Category.objects.create(**self.category)
        self.product['cat'] = Category.objects.first()
        Product.objects.create(**self.product)
        # добавление товара в корзину
        self.client.post(self.cart_url, {'quantity': '16'})
        # оформление заказа
        self.client.post(self.order_url, self.order)
        self.assertEqual(Order.objects.first().email, self.order.get('email'))
