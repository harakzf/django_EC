from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    '''何のためのメソッド？'''
    item_count = 0

    if 'admin' in request.path:     # リクエストのパスにadminが含まれていた場合（管理画面に遷移する場合）
        return []

    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))   # _cart_id()メソッド：引数requestで呼出し
            cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                item_count += cart_item.quantity

        except Cart.DoesNotExist:
            item_count = 0

    return dict(item_count=item_count)

