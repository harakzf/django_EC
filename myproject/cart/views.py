from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from order.models import Order, OrderItem

# 決済時用に以下インポート
import stripe
from django.conf import settings

# Create your views here.
# ※メソッドにはそれぞれ何かしらの意味、作成意図がある→そこを詰めていく方針が良いと思う

def _cart_id(request):
    '''セッションオブジェクトを保持/新規作成して返却するメソッド'''
    cart = request.session.session_key      # 生存している既存のセッションIDが存在すれば、それを格納

    if not cart:
        cart = request.session.create()  # セッションIDが存在しない場合、セッションオブジェクトを作成して保持

    return cart

def add_cart(request, product_id):      # product_idが引数として与えられる→この引数を処理するメソッド
    '''カート画面内の+ボタンの実装（数量+1機能実装）'''
    product = Product.objects.get(id=product_id)    # Productテーブルの主キーに対応するレコードを1件取得

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))        # セッションIDがcart_idに該当するCartテーブルのレコードを1件取得
    except Cart.DoesNotExist:                                       # 該当するレコードオブジェクトが存在しなかった場合、例外送出？
        cart = Cart.objects.create(cart_id = _cart_id(request))     # 与えられたセッションIDをcart_idとしてCartテーブルにレコードを新規作成
        cart.save()                                                 # .save()→ここで作成したレコードの保存

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)        # ()内の引数条件に該当するレコードオブジェクトを取得
        cart_item.quantity += 1                                             # 取得したオブジェクトの「quantity」カラムに+1する
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
    '''カート画面に対応するビュー'''
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

        cart_items = CartItem.objects.filter(cart=cart, active=True)    # CartItem（カート詳細）モデルオブジェクトから指定のレコードオブジェクトを取得

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

            # 注文書アプリ用に追加
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']

            customer = stripe.Customer.create(
                        email = email,
                        source = token
            )

            charge = stripe.Charge.create(
                        amount = stripe_total,
                        currency = 'GBP',
                        description = description,
                        customer = customer.id
            )

            '''注文書作成処理'''
            try:
                order_details = Order.objects.create(   # Order（注文書）モデルオブジェクトにレコードオブジェクトを1件新規作成

                        token = token,
                        total = total,
                        emailAddress = email,
                        billingName = billingName,
                        billingAddress1 = billingAddress1,
                        billingCity = billingCity,
                        billingPostcode = billingPostcode,
                        billingCountry = billingCountry,
                        shippingName = shippingName,
                        shippingAddress1 = shippingAddress1,
                        shippingCity = shippingCity,
                        shippingPostcode = shippingPostcode,
                        shippingCountry = shippingCountry

                    )
                order_details.save()

                for order_item in cart_items:
                    oi = OrderItem.objects.create(      # OrderItem（注文書詳細）モデルオブジェクトにレコードオブジェクトを1件新規作成

                            product = order_item.product.name,
                            quantity = order_item.quantity,
                            price = order_item.product.price,
                            order = order_details

                        )
                    oi.save()

                    '''発注または保存時に在庫を減らす処理'''
                    products = Product.objects.get(id=order_item.product.id)                # Product（商品）モデルのレコードオブジェクトを取得
                    products.stock = int(order_item.product.stock - order_item.quantity)    # 在庫減処理
                    products.save()
                    order_item.delete()

                    '''注文が保存されると、端末が以下メッセージを出力するように設定'''
                    print('注文が作成されました！')

                # return redirect('shop:allProdCat')                    # こちらだとショップ画面のまま遷移しない→お礼ページを出すため、以下の記述に修正
                return redirect('order:thanks', order_details.id)       # order:urls（app_name部分） thanks:urls(name部分)→エンドポイント（ビュー）に引数を与えてリダイレクト

            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
                return False,e

    # dict()：htmlテンプレートを返却したときのテンプレートタグへの代入変数を辞書型で定義
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))


def cart_remove(request, product_id):
    '''-ボタン実装（数量減機能）'''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(product=product, cart=cart)  # 該当するCartItemテーブルのレコードをオブジェクト化して取得（トランザクション開始）

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()            # 変更を加えたオブジェクトを保存（DBへの反映/レコード保存/commit(トランザクション終了)）

    else:                       # cart_itemの中身が1だった場合
        cart_item.delete()      # 0になることを同義なので、取得したオブジェクトを削除

    return redirect('cart:cart_detail')     # ビューへリダイレクト（app_name=XXXとpath(name=YYY)部分で指定）


def full_remove(request, product_id):
    '''削除ボタン（機能）実装'''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(product=product, cart=cart)

    # カート中身削除（上記のelse節と同様）
    cart_item.delete()

    return redirect('cart:cart_detail')
