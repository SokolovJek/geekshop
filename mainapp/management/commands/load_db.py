from adminapp.views import my_db_profile
from mainapp.models import Product
from django.db import connection
from django.core.management.base import BaseCommand
from django.db.models import F, When, Case, DecimalField, IntegerField, Q
from datetime import timedelta
from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_product = Product.objects.filter(Q(category__name='модерн') | Q(category__name='дом')).\
            select_related('category')
        # print(len(test_product))
        print(test_product)
        my_db_profile('load_db', '', connection.queries)


# select_related('category')
# {'sql': 'SELECT "mainapp_product".*, "mainapp_productcategory".* FROM "mainapp_product" INNER JOIN "mainapp_productcategory" ON '
#         '("mainapp_product"."category_id" = "mainapp_productcategory"."id") WHERE'
#         ' ("mainapp_productcategory"."name" = \'офис\' OR "mainapp_productcategory"."name" = \'модерн\')  LIMIT 21', 'time': '0.001'} ---- !!!! один запрос в БД

# not select_related('category')
# {'sql': 'SELECT mainapp_product".* FROM "mainapp_product" INNER JOIN "mainapp_productcategory" ON
#       ("mainapp_product"."category_id" = "mainapp_productcategory"."id") WHERE
#       ("mainapp_productcategory"."name" = \'офис\' OR "mainapp_productcategory"."name" = \'модерн\')  LIMIT 21', 'time': '0.001'}   ---- !!!!! 6 запросов в БД



# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         """«Сonditional-expressions» - логика на уровне QuerySet"""
#         ACTION_1 = 1
#         ACTION_2 = 2
#         ACTION_EXPIRED = 3
#
#         action_1__time_delta = timedelta(hours=12)
#         action_2__time_delta = timedelta(days=1)
#
#         action_1__discount = 0.3
#         action_2__discount = 0.15
#         action_expired__discount = 0.05
#
#         action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
#
#         action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) &\
#                               Q(order__updated__lte=F('order__created') + action_2__time_delta)
#
#         action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)
#
#         action_1__order = When(action_1__condition, then=ACTION_1)
#         action_2__order = When(action_2__condition, then=ACTION_2)
#         action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)
#
#         action_1__price = When(action_1__condition,
#                   then=F('product__price') * F('quantity') * action_1__discount)
#
#         action_2__price = When(action_2__condition,
#                   then=F('product__price') * F('quantity') * -action_2__discount)
#
#         action_expired__price = When(action_expired__condition,
#                   then=F('product__price') * F('quantity') * action_expired__discount)
#
#         test_orderss = OrderItem.objects.annotate(
#            action_order=Case(
#                action_1__order,
#                action_2__order,
#                action_expired__order,
#                output_field=IntegerField(),
#            )).annotate(
#            total_price=Case(
#                action_1__price,
#                action_2__price,
#                action_expired__price,
#                output_field=DecimalField(),
#            )).order_by('action_order', 'total_price').select_related()
#
#         for orderitem in test_orderss:
#            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
#                    {orderitem.product.name:15}: скидка\
#                    {abs(orderitem.total_price):6.2f} руб. | \
#                {orderitem.order.updated - orderitem.order.created}')