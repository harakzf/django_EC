from django.db import models

# 追記
from django.urls import reverse

# Create your models here.
'''モデルの詳細解説'''
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)   # 小 - 大サイズの文字列のフィールド
    slug = models.SlugField(max_length=250, unique=True)   # 文字/数字/アンダースコア/ハイフンのみを含む短いラベル。 一般的に URL 内で使用される ※slugについてはもう少し要調査
    description = models.TextField(blank=True)
    # ①ImageFieldを扱うにはPillowが必要→パッケージインストール
    # settings.pyにMEDIA_ROOTを定義する必要
    image = models.ImageField(upload_to='category', blank=True)     # FileField から全ての属性とメソッドを継承→アップロードされたオブジェクトが有効な画像であることを検証する
    '''
    ImageField：画像ファイルを簡単に扱うためのフィールド
    upload_to=<ディレクトリ名>で引数を指定することで、MEDIA_ROOT/<ディレクトリ名>/<画像ファイル名>で保存される

    '''

    '''
    slug→

    '''


    class Meta:
        '''テーブルのメタ情報を設定'''
        ordering = ('name',)                  # 並び替えを実施する変数。'name'をデフォルト（昇順）で表示させる
        verbose_name = 'category'             # テーブルの表示名。以下で指定しないとココの複数形がadmin画面に表示される
        verbose_name_plural = 'カテゴリー'    # テーブルの表示名（複数形）。admin画面に複数形で表示される時の名称指定

    # 追記①→ImageFieldを与えたときにオーバライドされるメソッド。
    def get_url(self):
        return reverse('shop:products_by_category', args = [self.slug])     # ??

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    # PK：idカラム（MySQL参照）→「product_id」と表記される
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = '商品'

    # 追記②
    def get_url(self):
        return reverse('shop:ProdCatDetail', args=[self.category.slug, self.slug])


    def __str__(self):
        return '{}'.format(self.name)
