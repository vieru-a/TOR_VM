from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from TOR_VM_store.models import Product


# анонимный юзер/юзер
class Order(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone_number = PhoneNumberField(verbose_name='Номер телефона',
                                    error_messages={"unique": "Пользователь с таким номером уже существует.",
                                                    "invalid": "Введите корректный номер телефона (+79999999999)"})
    email = models.EmailField(max_length=150, verbose_name='E-mail')
    address1 = models.CharField(max_length=255, verbose_name='Адрес')
    city = models.CharField(max_length=150, verbose_name='Город')
    country = CountryField(default='RU', verbose_name='Страна')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Пользователь')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Номер заказа - {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('TOR_VM_store.Product', on_delete=models.PROTECT, related_name='order_items',
                                verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.product.name)

    def get_cost(self):
        return self.price * self.quantity
