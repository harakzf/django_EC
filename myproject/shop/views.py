from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views import View


# 追加（ページネータ機能追加）
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class IndexView(View):
    def get(self, request):                 # 汎用ビューを使用するときは、用意されているget()メソッドを使用しなければならない
        context = {'sample': 'テストページ'}

        return render(request, 'sample.html', context)


# カテゴリーView（トップページ）
class allProdCatView(View):
    def get(self, request, c_slug=None):    # getリクエストで受け取る
        c_page = None
        products_list = None

        if c_slug != None:  # c_slug=1のように、引数に数が与えられた状態でViewに入った場合に実行
            '''
            get_object_or_404()：モデルに対してget()を呼び出して、オブジェクトを1件取得する
                →モデルが見つからない場合は、django.http.Http404を送信して画面がPage not found(404)ページに遷移される
            '''
            c_page = get_object_or_404(Category, slug=c_slug)                   # 第一引数：モデルのクラス名、第二引数：任意の値→c_page：「3」が入る
            products_list = Product.objects.filter(category=c_page, available=True)  # ??

        else:
            '''
            <モデルクラス（DBテーブル）名>.object.<クエリメソッド（クエリAPI）>
            ※「クエリセット」部分はDjangoGirls復習
            '''
            products_list = Product.objects.all().filter(available=True)  # ??

        # 追加
        '''Pagination code'''
        paginator = Paginator(products_list, 6)
        try:
            page = int(request.GET.get('page','1'))
        except:
            page = 1
        try:
            products = paginator.page(page)
        except (EmptyPage, InvalidPage):
            products = paginator.page(paginator.num_pags)


        context = {'category': c_page, 'products': products}

        return render(request, 'shop/category.html', context)

# 商品詳細View
class ProdCatDetailView(View):
    def get(self, request, c_slug, product_slug):
        try:
            # どうやら以下の__部分はダブルアンスコで動作するらしい・・・なぜ？？
            product = Product.objects.get(category__slug=c_slug, slug=product_slug)  # DBからの取得データを変数に保持

        except Exception as e:
            raise e

        context = {'product': product}

        return render(request, 'shop/product.html', context)


# index = IndexView.as_view()
# allProdCat = allProdCatView.as_view()
# ProdCatDetail = ProdCatDetailView.as_view()
