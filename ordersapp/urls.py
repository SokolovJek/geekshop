from django.urls import path
import ordersapp.views as ordersapp


app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    path('order_create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    path('order_update/<int:pk>/', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    path('order_delete/<int:pk>', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('order_detail/<int:pk>', ordersapp.OrderDetail.as_view(), name='order_detail'),
    path('make_order/<int:pk>', ordersapp.change_status_for_order, name='change_status_for_order')
]