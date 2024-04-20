from django.shortcuts import get_object_or_404, redirect

from django.views.generic import FormView

from TOR_VM_store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


class CartDetail(FormView):
    form_class = CartAddProductForm
    template_name = 'cart/detail.html'
    extra_context = {'nav_selected': 2}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class CartAdd(FormView):
    form_class = CartAddProductForm
    template_name = 'cart/detail.html'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart:cart_detail')


class CartRemove(FormView):
    form_class = CartAddProductForm
    template_name = 'cart/detail.html'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart.remove(product)
        return redirect('cart:cart_detail')
