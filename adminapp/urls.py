from django.urls import path, include
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.UsersList.as_view(), name='index'),
    path('user_delete/<int:pk>', adminapp.user_delete, name='user_delete'),
    path('user_update/<int:pk>', adminapp.user_update, name='user_update'),
    path('user_create/', adminapp.user_create, name='user_create'),

    path('categories/', adminapp.categories, name='categories'),
    path('categories/create/', adminapp.CategoriesCreateView.as_view(), name='categories_create'),
    path('categories/update/<int:pk>', adminapp.CategoryUpdateView.as_view(), name='categories_update'),
    path('categories/delete/<int:pk>', adminapp.categories_delete, name='categories_delete'),



    path('categories/<int:pk>/products', adminapp.product_list, name='product_list'),
    path('categories/products_update/<int:pk>', adminapp.product_update, name='product_update'),
    path('categories/product_delete/<int:pk>', adminapp.product_delete, name='product_delete'),
    path('categories/<int:category_pk>/product_create', adminapp.product_create, name='product_create'),

    path('orders/', adminapp.OrderList.as_view(), name='orders_list'),
    path('orders/orders_status_change/<int:pk>', adminapp.OrderStatusUpdate.as_view(), name='orders_status_change'),
]