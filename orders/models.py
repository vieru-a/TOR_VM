from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from TOR_VM_store.models import Product


# анонимный юзер/юзер
class Order(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone_number = PhoneNumberField(verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='E-mail')
    address1 = models.CharField(max_length=255, verbose_name='Адрес')
    city = models.CharField(max_length=150, verbose_name='Город')
    country = CountryField(default='RU', verbose_name='Страна')

    # СВЯЗЬ С ПОЛЬЗОВАТЕЛЕМ

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self, request):
        print(request.get('user'))
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('TOR_VM_store.Product', on_delete=models.PROTECT, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
