from django.shortcuts import render
from django.http import Http404

from commerce.models.orders import Order

def order_status(request, order_id):
    try:
        order = Order.objects.get(uuid=order_id)
    except Order.DoesNotExist:
        raise Http404
    return render(request, 'orders_ws.html', {'order': order})