from django.contrib import admin
from .models import Category, Product

# クラスベースへの書き方に変更する
# admin.site.register(Category)
# admin.site.register(Product)

class CategoryAdmin(admin.ModelAdmin):
    '''adminページでの設定画面の調整←本設定でadminページの画面を調整する'''
    list_display = ['name', 'slug']     # 画面カラム設定
    prepopulated_field = {'slug':('name',)}     # ???

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']     # 詳細画面を開かなくても直接画面で編集ができる
    prepopulated_field = {'slug':('name',)}     # ???
    list_per_page = 20              # ???

admin.site.register(Product, ProductAdmin)



