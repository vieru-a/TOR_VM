from rest_framework import serializers

from .models import Product


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'article_number', 'image', 'price', 'description', 'cat')
