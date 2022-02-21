from django.shortcuts import render
from basketapp.models import BasketModel
from mainapp.models import Product
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from authapp.models import ShopUser
from django.urls import reverse
from django.db.models import F




# Теперь при попытке добавить товар в корзину Django проверит свойство .is_authenticated(@login_required)
# у объекта пользователя. Если оно True — товар добавится,
# иначе произойдет переход по адресу из константы LOGIN_URL.(LOGIN_URL = '/auth/login/')
#  "GET /auth/login/?next=/basket/basketadd/17/ HTTP/1.1" 200 1609 - при попытки добавитьтовар в корзину не залогиненым
@login_required
def basket(request):
    user_basket = BasketModel.objects.filter(user=request.user).select_related()
    content = {
        'title': 'Корзина',
        'user_basket': user_basket
    }
    return render(request, 'basketapp/basket.html', context=content)


# прописали в settings.py константу LOGIN_URL = '/auth/login/', для перехода на указанную страницу(в нашем случае это
# '/auth/login/' )
# <HttpResponseRedirect status_code=302, "text/html; charset=utf-8", url="http://127.0.0.1:8000/auth/login(<--вот он)
# /?next=/basket/basketadd/12/">
@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('mainapp:product', args=[pk]))
    else:
        basket_item = BasketModel.get_product(user_id=request.user.pk, product_id=pk)
        if basket_item:
            basket_item.update(quantity=F('quantity') + 1)    # update - чтобы сделать один запрос а не два
            # basket_item.quantity = F('quantity') + 1
            # basket_item.save()
        else:
            BasketModel.objects.create(user=request.user, product=Product.objects.filter(pk=pk).first(), quantity=1)

        return HttpResponseRedirect(reverse('mainapp:index'))
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    prod_remove = BasketModel.objects.filter(pk=pk).first()
    prod_remove.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_quantity(request, pk, qty):
    if request.is_ajax():
        basket = BasketModel.objects.filter(pk=pk).first()
        if basket:
            if pk == 0:
                basket.delete()
            else:
                basket.quantity = qty
                basket.save()
            change = render_to_string('basketapp/includes/basket_summary.html', request=request)
            price = f'{round(basket.product_cost())}&nbspрублей'
            return JsonResponse({
                'status': True,
                'change': change,
                'change_price': price
            })
        else:
            return JsonResponse({
                'status': False,
            })
