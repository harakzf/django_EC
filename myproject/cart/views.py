from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# 決済時用に以下インポート
import stripe
from django.conf import settings

# Create your views here.
# ※メソッドにはそれぞれ何かしらの意味、作成意図がある→そこを詰めていく方針が良いと思う

def _cart_id(request):
    '''セッションオブジェクトを保持/新規作成して返却するメソッド'''
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()  # セッションオブジェクトを作成して保持

    return cart

def add_cart(request, product_id):      # product_idが引数として与えられる→この引数を処理するメソッド
    '''カート画面内の+ボタンの実装'''
    product = Product.objects.get(id=product_id)    # 与えられた引数に相当するProductテーブルのレコードを1件取得（id検索）

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))   # リクエストされたカートIDに紐づくモデルオブジェクト（レコード）を取得→変数保持
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save() # .save()→レコードの保存

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)        # 既存レコード取得→変数保持
        cart_item.quantity += 1     # 作成レコードの「quantity」カラムに+1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
        cart_item.save()

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    # 以下追記（決済時に使用）
    stripe.api_key = settings.STRIPE_SECRET_KEY     # stripeパッケージ中のapi_keyに設定ファイルで設定したシークレットキー設定
    stripe_total = int(total * 100)
    description = 'My First Dress Shop - New Order'    # 文字列を変数に代入
    data_key = settings.STRIPE_PUBLISHABLE_KEY      # 公開キーを設定

    if request.method == 'POST':    # リクエストのメソッドがPOSTの場合
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']

            customer = stripe.Customer.create(
                        email = email,
                        source = token
            )

            charge = stripe.Charge.create(
                        amount = stripe_total,
                        currency = 'jpy',
                        description = description,
                        customer = customer.id
            )

        except stripe.error.CardError as e:
                return False,e

    return render(request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter, data_key = data_key, stripe_total = stripe_total, description = description))


def cart_remove(request, product_id):
    '''-ボタン実装'''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)  # モデル（DB）の構造が理解できていない・・・

    if cart_item.quantity > 1:
        cart_item.quantity -= 1 # 数量マイナス
        cart_item.save()    # レコード保存

    else:           # cart_itemの中身が1だった場合
        cart_item.delete()      # 0になることを同義なので、カートの中身を削除

    return redirect('cart:cart_detail')


def full_remove(request, product_id):
    '''削除ボタン実装'''
    # 上記（-ボタン実装時）と同手順
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    # カート中身削除
    cart_item.delete()

    return redirect('cart:cart_detail')
