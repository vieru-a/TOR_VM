from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'city', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
