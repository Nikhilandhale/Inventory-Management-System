from django.urls import path

from . import views
from .views import UserProfileView

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='dashboard_index'),
    path('add-products/', views.add_products, name='add_products'),
    path('search-products/', views.search_available_products, name='search_available_products'),
    path('view-available-products/', views.view_available_products, name='view_available_products'),
    path('sell-available-products/', views.sell_available_products, name='sell_available_products'),
    path('view-sold-products/', views.view_sold_products, name='view_sold_products'),
    path('users/', views.users, name='users'),
    path('remove_user/', views.remove_user, name='remove_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('product_list/', views.product_list, name='product_list'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('shop-products/', views.shop_products, name='shop_products'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
