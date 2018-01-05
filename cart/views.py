from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from cupons.forms import CuponApllyForm
from cupons.models import Cupon


# строки 15-16 и 23-25 отключают редирект в корзину при покупке товара

@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    # from_page = request.META['HTTP_REFERER']
    # from_p = str(from_page)[-6:]
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    # if from_p != '/cart/':
    #     return redirect(from_page)
    return redirect('cart:CartDetail')

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')


def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    cupon_apply_form = CuponApllyForm()
    has_cupons = Cupon.objects.filter(active=True).count()
    return render(request, 'cart_detail.html',
                 {'cart': cart, 'cupon_apply_form': cupon_apply_form, 'has_cupons': has_cupons})
