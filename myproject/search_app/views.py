from django.shortcuts import render
from shop.models import Product
from django.db.models import Q

'''
本アプリは検索機能に特化したアプリ。
→DBモデル等は作らず、viewとurl、templateのみの実装→分かりやすい！
'''

def searchResult(request):
    products = None
    query = None

    if 'q' in request.GET:
        query = request.GET.get('q') # リクエストの内容（検索内容）を保持
        products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))

    return render(request, 'search.html', {'query': query, 'products': products})
        # search.htmlにはテンプレートタグ（query, products）を保持する必要がある



