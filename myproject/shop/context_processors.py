from .models import Category

'''
リンクのやりとりをするモジュール。
※どうやらこのモジュールはまだ使用されていないっぽい・・・
'''

def menu_links(request):
    links = Category.objects.all()  # 「カテゴリ」テーブルから全データ取得

    return dict(links = links)      # ???
    print(dict(links=links))

# print関数使ってみるのもよい（試行）
# 本モジュールを生成した後、settings.py編集（template設定部分）