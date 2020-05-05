from django.urls import path
from .products import product_views


app_name = 'shop'

urlpatterns = [
    path('', product_views.product_list, name='product_list'),
    path('<slug:category_slug>/', product_views.product_list,
         name='product_list_by_category'),
    path('<int:product_id>/<slug:slug>/', product_views.product_detail,
         name='product_detail'),
]
