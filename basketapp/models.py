from django.db import models
from authapp.models import ShopUser
from mainapp.models import Product
from django.contrib.auth import get_user_model


class BasketModel(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='basket')

    # можно было и без related_name='basket' но с ней можно обращатся на прямую -> {{ user.basket.all }}
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    # product = models.CharField(verbose_name='название продукта', max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    time_add = models.TimeField(verbose_name='время изменения', auto_now=True)
    time_create = models.TimeField(verbose_name='время добавления', auto_now_add=True)

    def product_cost(self):
        return self.product.price * self.quantity

    def get_product(user_id, product_id):
        return BasketModel.objects.filter(user=user_id, product=product_id)

    """коректировка остатка на складе при покупке или заказе -- аналог работы через сигналы"""
    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     item = BasketModel.objects.filter(pk=self.pk).first()
    #     if item is not None:
    #         self.product.quantity -= self.quantity - item.quantity
    #         self.product.save()
    #     else:
    #         self.product.quantity -= self.quantity
    #         self.product.save()
    #     super().save(*args, **kwargs)

    def get_item(id):
        print('i am here', id)
        item = BasketModel.objects.filter(pk=id).first()
        return item