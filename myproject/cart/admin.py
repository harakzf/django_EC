from django.contrib import admin
from .models import Cart, CartItem

# 今回は管理画面に以下テーブル表示しない
admin.site.register(Cart)
admin.site.register(CartItem)


