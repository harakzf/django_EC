from django.shortcuts import render, get_object_or_404
from .models import Order


# 注文IDが存在する場合に起動
def thanks(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)

    return render(request, 'thanks.html', {'customer_order':customer_order})