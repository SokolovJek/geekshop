from django.urls import path, include
import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('api/', mainapp.GetProductInfoView.as_view(), name='main_api'),
    path('products/', mainapp.categories, name='products'),
    path('contact/', mainapp.contact, name='contact'),
    path('category/<int:pk>/', mainapp.categories, name='category'),
    path('products/<int:pk>/', mainapp.product, name='product'),
    path('category/<int:pk>/page/<int:page>/', mainapp.categories, name='page'),

]