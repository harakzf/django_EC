
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [

    path('', views.allProdCat, name='allProdCat'),
    # slug：1が代入された状態で接続されたら、以下のURLに遷移する意（例：c_slug=1）
    path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/', views.ProdCatDetail, name='ProdCatDetail'),

    ]


