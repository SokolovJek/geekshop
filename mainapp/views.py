from django.shortcuts import render
from mainapp.models import ProductCategory, Product
import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer

from django.conf import settings
from django.core.cache import cache


def get_products_for_cache():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True)


def get_category_for_cache():
    if settings.LOW_CACHE:
        key = 'category'
        category = cache.get(key)
        if category is None:
            category = ProductCategory.objects.filter(is_active=True)
            cache.set(key, category)
        return category
    else:
        return ProductCategory.objects.filter(is_active=True)


# function for get all products without hot_product
def get_products(pk_category):
    products = get_products_for_cache()
    if pk_category == 0:
        hot_product = random.choice(products)
        without_hot = products.exclude(pk=hot_product.pk)
    else:
        hot_product = random.choice(products.filter(category_id=pk_category))
        without_hot = products.filter(category_id=pk_category).exclude(pk=hot_product.pk)
    return hot_product, without_hot


def contact(request):
    content = {
        'title': 'контакты'
    }
    return render(request, 'mainapp/contact.html', context=content)


def index(request):
    prod = get_products_for_cache()
    content = {
        'title': 'главная',
        'products_images': prod,
    }
    return render(request, 'mainapp/index.html', context=content)


def categories(request, pk=0, page=1):
    category = get_category_for_cache()
    hot_product, without_hot = get_products(pk)
    if pk == 0:
        title = 'все продукты'
    else:
        title = ProductCategory.objects.get(pk=pk).name

    paginator = Paginator(without_hot, 2)
    try:
        product_paginator = paginator.page(page)
    except PageNotAnInteger:
        product_paginator = paginator.page(1)
    except EmptyPage:
        product_paginator = paginator.page(paginator.num_pages)
    content = {
        'title': title,
        'category': category,
        'pk': pk,
        'hot_product': hot_product,
        'with_out_hot': product_paginator,
        'product_paginator': product_paginator
    }
    return render(request, 'mainapp/products.html', context=content)


def product(request, pk):
    select_prod = Product.objects.filter(pk=pk).first()
    content = {
        'pk': pk,
        'product': select_prod
    }
    return render(request, 'mainapp/product.html', context=content)


class GetProductInfoView(APIView):
    # в контроллере запускается метод, чьё имя совпадает с именем метода поступившего http - запроса в нижнем регистр
    # в нашем случае GET.
    def get(self, request):
        # Получаем набор всех записей из таблицы Product
        queryset = Product.objects.all()
        # queryset = Product.objects.first() --> many=False
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = ProductSerializer(
            instance=queryset, # Передаём набор записей
            many=True # Указываем, что на вход подаётся именно набор записей
        )
        # рендеринг в json  формат происходит под капотом в классе APIVIEW
        return Response(serializer_for_queryset.data)







