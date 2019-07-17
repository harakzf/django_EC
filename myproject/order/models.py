from django.db import models

# Orderテーブル
class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='GRP Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)        #請求名
    billingAddress1 = models.CharField(max_length=250, blank=True)    #            # カラムの型を指定しているのみ
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=10, blank=True)
    shippingPostcode = models.CharField(max_length=200, blank=True)
    shippingCountry = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'Order'          # mysqlでのテーブル名定義
        ordering = ['-created']     # 「created」カラムの昇順？での表示を指示
        verbose_name = 'Order'
        verbose_name_plural = '注文管理'

    def __str__(self):
        return str(self.id)         # adminページではカラムの主キーを表示

# OrderItem（請求書詳細）テーブル
class OrderItem(models.Model):
    product = models.CharField(max_length=250)                                                  # 商品
    quantity = models.IntegerField()                                                            # 数量
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='GRP Price')      # 価格
    order = models.ForeignKey(Order, on_delete=models.CASCADE)                                  # orderテーブル参照


    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):                    # テンプレートで呼び出すときに使用
        return self.quantity * self.price

    def __str__(self):
        return self.product

