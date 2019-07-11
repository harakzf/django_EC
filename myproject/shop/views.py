from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product

# 追加（ページネータ機能追加）
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
# タスク１：View関数のクラス化

def index(request):
    text_var = 'This is my first web page.'
    return HttpResponse(text_var)       # httpresponseを返却

# カテゴリーView
def allProdCat(request, c_slug=None):
    # 初期値設定
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

    return render(request, 'shop/category.html', {'category': c_page, 'products': products})

# 投稿ページ詳細View
def ProdCatDetail(request, c_slug, product_slug):
    try:
        # どうやら以下の__部分はダブルアンスコで動作するらしい・・・なぜ？？
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)  # DBからの取得データを変数に保持

    except Exception as e:
        raise e

    # テンプレートタグ「product」に、保持したオブジェクトを表示させる→テンプレートに渡す
    return render(request, 'shop/product.html', {'product': product})


