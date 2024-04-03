from django.shortcuts import render
from django.views.generic import FormView

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


class OrderCreate(FormView):
    form_class = OrderCreateForm
    template_name = 'orders/create.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart, 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if request.user.is_authenticated:
            user = request.user
            anon_user = {'first_name': user.first_name,
                         'last_name': user.last_name,
                         'phone_number': user.phone_number,
                         'email': user.email,
                         'address1': user.address1,
                         'city': user.city,
                         'country': user.country}
            form = self.form_class(anon_user)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # на почту не приходит письмо
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/created.html', {'order': order})
