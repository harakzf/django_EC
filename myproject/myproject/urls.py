
from django.contrib import admin
from django.urls import path, include
from shop import views      # アプリを指定してインポートできる→Oscarアプリ作成時に参考

from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('shop/', include('shop.urls')),
    path('search/', include('search_app.urls')),    # 追加（検索アプリ遷移用）
    path('cart/', include('cart.urls')),            # 追加（カートアプリ用）
]

# DEBUGモードがTRUEの場合
# どうやら以下を追記することでHP上に画像を表示させることができるらしい→画像をクリックしてアクセスすることも可
if settings.DEBUG:
    # staticファイルとmediaファイルのドキュメントルートを設定
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)