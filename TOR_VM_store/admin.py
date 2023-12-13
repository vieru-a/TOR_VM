from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'article_number', 'name', 'get_html_photo', 'price', 'cat', 'is_available')
    list_display_links = ('id', 'article_number', 'name', 'cat')
    ordering = ['id', 'is_available']
    list_editable = ('is_available',)
    prepopulated_fields = {'slug': ('article_number',)}
    fields = ('article_number', 'name', 'slug', 'price', 'is_available', 'cat', 'description', 'image', 'get_html_photo')
    readonly_fields = ('get_html_photo', )

    def get_html_photo(self, obj):
        return mark_safe(f"<a href='{obj.image.url}'><img src='{obj.image.url}' width=150")

    get_html_photo.short_description = 'Превью фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'parent', 'get_html_photo')
    list_display_links = ('id', 'name', 'parent')
    ordering = ['id']
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'type', 'parent', 'description', 'image', 'get_html_photo')
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, obj):
        return mark_safe(f"<a href='{obj.image.url}'><img src='{obj.image.url}' width=80")

    get_html_photo.short_description = 'Превью фото'
