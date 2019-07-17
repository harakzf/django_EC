
from django.contrib import admin
from django.urls import path, include
# from shop import views      # アプリを指定してインポートできる→Oscarアプリ作成時に参考
from shop.views import IndexView

from . import settings
from django.conf.urls.static import static

# 追加（admin表示画面修正）
admin.site.site_title = '管理者ページ'
admin.site.site_header = 'R&D 管理サイト'
admin.site.index_title = 'メニュー'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index, name='index'),
    path('', IndexView.as_view(), name='sample_view'),
    path('shop/', include('shop.urls')),
    path('search/', include('search_app.urls')),    # 追加（検索アプリ遷移用）
    path('cart/', include('cart.urls')),            # 追加（カートアプリ用）
    path('order/', include('order.urls')),          # 追加（注文アプリ用）
]

# DEBUGモードがTRUEの場合
# どうやら以下を追記することでHP上に画像を表示させることができるらしい→画像をクリックしてアクセスすることも可
if settings.DEBUG:
    # staticファイルとmediaファイルのドキュメントルートを設定
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)