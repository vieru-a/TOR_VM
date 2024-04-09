from django.test import TestCase
from django.urls import reverse_lazy

from TOR_VM_store.models import Product, Category


class CartTest(TestCase):
    def setUp(self):
        self.cart_url = reverse_lazy('cart:cart_add', kwargs={'product_id': 1})
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

        return super().setUp()

    def test_view_correctly(self):
        """Проверка доступа к странице"""
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')

    def test_cart(self):
        """Проверка добавления товара в корзину"""
        Category.objects.create(**self.category)
        self.product['cat'] = Category.objects.first()
        Product.objects.create(**self.product)
        # добавление товара в корзину
        response = self.client.post(self.cart_url, {'quantity': '16'})
        cart_price = self.client.session.get('cart')['1']['price']

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/cart_detail/')
        self.assertEqual(cart_price, '209.00')
