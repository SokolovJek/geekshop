from django.db import models
from django.conf import settings
from mainapp.models import Product
from authapp.models import ShopUser


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='дата обновления', auto_now=True)
    statys = models.CharField(verbose_name='статус', max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='Активен', db_index=True, default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    def get_total_summary(self):
        """метод для вывода общей цены и количества элементов связаных с заказом, и далнейшее кэширование его
        с помощью тега WITH"""
        items = self.orderitems.select_related()     # при помощи метода «select_related()» находим все элементы заказа:
        get_total_quantity = sum(list(map(lambda x: x.quantity, items)))
        get_total_cost = sum(list(map(lambda x: x.quantity * x.product.price, items)))
        return {
            'get_total_quantity': get_total_quantity,
            'get_total_cost': get_total_cost,
        }

    # def get_total_quantity(self):
    #     items = self.orderitems.select_related()     # при помощи метода «select_related()» находим все элементы заказа:
    #     return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)
    #
    # def get_total_cost(self):
    #     items = self.orderitems.select_related()
    #     return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    """коректировка остатка на складе при покупке или заказе -- аналог работы через сигналы"""
    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     item = OrderItem.objects.filter(pk=self.pk).first()
    #     if item is not None:
    #         self.product.quantity -= self.quantity - item.quantity
    #         self.product.save()
    #     else:
    #         self.product.quantity -= self.quantity
    #         self.product.save()
    #     super().save(*args, **kwargs)

    def get_item(id):
        """метод для сигналов"""
        print('i am here', id)
        item = OrderItem.objects.filter(pk=id).first()
        return item