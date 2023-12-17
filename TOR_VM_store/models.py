import os

from django.urls import reverse
from transliterate import translit

from django.db import models
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey


def get_slug(slug, model):
    unique_slug = slug
    number = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{number}'
        number += 1

    return unique_slug


def get_image_path(instance, filename):
    if isinstance(instance, Category):
        upload_dir = os.path.join(instance.name)
        if os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        return os.path.join(upload_dir, filename)
    else:
        upload_dir = os.path.join(instance.cat.name, instance.name)
        if os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        return os.path.join(upload_dir, filename)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to=get_image_path, max_length=255, verbose_name='Изображение продукта')
    article_number = models.CharField(max_length=255, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(max_length=1000, verbose_name='Описание товара')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    cat = TreeForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_string = translit(f'{self.article_number}', 'ru', reversed=True)
            self.slug = get_slug(slug_string, Product)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.article_number

    def get_absolute_url(self):
        return reverse('store_product_detail', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(MPTTModel):
    SUBCATEGORY = 'subcategory'
    CATEGORY = 'category'

    type_choices = [(SUBCATEGORY, 'Подкатегория'),
                    (CATEGORY, 'Категория')]

    name = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to=get_image_path, max_length=255, verbose_name='Изображение категории')
    description = models.TextField(max_length=1000, verbose_name='Описание категории')
    type = models.CharField(choices=type_choices, max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_string = translit(self.name, 'ru', reversed=True)
            self.slug = get_slug(slugify(slug_string), Category)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store_category_detail', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
