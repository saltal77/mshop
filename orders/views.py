from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.template.loader import get_template
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context

def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.cupon:
                order.cupon = cart.cupon
                order.discount = cart.cupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            MailCreatedOrder(order.id)
            return render(request, 'created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'create.html', {'cart': cart,
      
                                                        'form': form})
@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_order_detail.html', {'order': order})

@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
               stylesheets=[weasyprint.CSS('static/css/bootstrap.min.css')])
    return response

def MailCreatedOrder(order_id):
    """
    Отправка Email сообщения о создании покупке
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ c номером {} из магазина МедОдежды'.format(order.id)
    msgtext = get_template('mail_order_detail.html').render({ 'order': order, })
    msg = EmailMultiAlternatives(subject, msgtext, settings.SERVER_EMAIL, (order.email, settings.STUFF_EMAIL))
    msg.attach_alternative(msgtext, "text/html")
    mail = msg.send()
    return mail