from django.db import models
from shop.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)    # auto_now_add：モデルインスタンスを保存するタイミングで更新（True）

    class Meta:
        db_table = 'cart'
        ordering = ['date_added']
#         verbose_name = 'cart'        # 本テーブルは管理画面で管理する必要が無いため、テーブル表示しない
#         verbose_name_plural = 'カート'

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    '''
    on_detele：
        参照するオブジェクトが削除されたときに、それと紐づけられたオブジェクトも一緒に削除するのか、
        それともそのオブジェクトは残しておくのかを設定するもの。
    CASCADE：
        削除するオブジェクトに紐づいたオブジェクトを全て削除する
    ※FKの使用方法
    ※MySQLの中身の見方
    '''

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()        # おそらくカートの中に入っている商品の個数を示している
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'
#         verbose_name = 'cartItem'
#         verbose_name_plural = 'カートアイテム一覧'


    def sub_total(self):    # ???
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


