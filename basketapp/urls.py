from django.contrib import admin
from django.urls import path, include
import basketapp.views as basketapp
from django.conf import settings
from django.conf.urls.static import static


app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='basket'),
    path('basketadd/<int:pk>/', basketapp.basket_add, name='basketadd'),
    path('basketremove/<int:pk>/', basketapp.basket_remove, name='basketremove'),
    # '/basket/change_quantity/' + productPk + '/' +  qty + '/',
    path('change_quantity/<int:pk>/<int:qty>/', basketapp.change_quantity),
]