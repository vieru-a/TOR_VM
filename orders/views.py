from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created


class OrderCreate(CreateView):
    form_class = OrderCreateForm
    template_name = 'orders/create.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart, 'form': self.form_class, 'nav_selected': 2})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        order = None
        if request.user.is_authenticated:
            user = request.user
            order = Order.objects.create(first_name=user.first_name,
                                         last_name=user.last_name,
                                         phone_number=user.phone_number,
                                         email=user.email,
                                         address1=user.address1,
                                         city=user.city,
                                         country=user.country,
                                         user=user)
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                order = form.save()
            else:
                return render(request, self.template_name, {'cart': cart, 'form': form, 'nav_selected': 2})

        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        order_created.delay(order.id)
        return render(request, 'orders/created.html', {'order': order, 'nav_selected': 2})
