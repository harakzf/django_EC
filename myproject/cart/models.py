from django.db import models
from shop.models import Product

# Create your models here.
class Cart(models.Model):       # PK（id）は自動設定（モデルの性質）
    '''
    カートそのものを管理するテーブル。
    カラムとしてcart_id=セッションIDが紐づけられる
    '''
    cart_id = models.CharField(max_length=250, blank=True)      # ここでは単に格納されるデータ型（箱）を定義しているだけ
    date_added = models.DateField(auto_now_add=True)            # auto_now_add：モデルインスタンスを保存するタイミングで更新（True）→DBに反映されている

    class Meta:
        db_table = 'cart'
        ordering = ['date_added']
        verbose_name = 'cart'
        verbose_name_plural = 'カート管理'

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    '''
    カート内の商品の状態を管理するテーブル。

    on_detele：
        参照するオブジェクトが削除されたときに、それと紐づけられたオブジェクトも一緒に削除するのか、
        それともそのオブジェクトは残しておくのかを設定するもの。
    CASCADE：
        削除するオブジェクトに紐づいたオブジェクトを全て削除する
    '''

    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 商品をFKで指定
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)        # その商品の入っているカートをFKで指定
    quantity = models.IntegerField()                                # おそらくカートの中に入っている商品の個数を示している
    active = models.BooleanField(default=True)                      # データ型（箱）のみ定義

    class Meta:
        db_table = 'CartItem'                                       # DBに登録されるテーブル名を定義
        verbose_name = 'cartItem'
        verbose_name_plural = 'カートアイテム管理'                  # adminページへの表記文字を定義


    def sub_total(self):                                           # htmlでオブジェクトのメソッドとして呼び出せるよう設定
        return self.product.price * self.quantity

#     def __str__(self):
#         return self.product


