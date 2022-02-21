from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import HttpResponseRedirect, reverse
from django.shortcuts import HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from basketapp.models import BasketModel
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem
from authapp.models import ShopUser

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class OrderList(ListView):
    """По умолчанию Django будет искать шаблон с именем вида «<имя класса>_list.html"""
    model = Order
    # context_object_name = 'posts'   # Если в шаблоне вместо object_list мы хотим использовать другое обозначение
    extra_context = {'title': 'ваши заказы'} # передаем загаловок
    # template_name = 'my_template.html' # если есть необхадимость задать имя шаблона
    # get_template_names()  Данный метод возвращает список имен шаблонов, которые Django будет пытаться
    #                                                           использовать в порядке их указания

    def get_queryset(self):
        """по умолчанию данный метод выводит в форму все обьекты указзанной модели, но его можно переопределить чтоб
        он удовлетворял наши подребности"""
        item = Order.objects.filter(user=self.request.user)
        return item

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


class OrderItemsCreate(CreateView):
    """По умолчанию при использовании классов CreateView и UpdateView шаблон
    должен иметь имя вида «<имя класса>_form.html»:"""
    model = Order
    extra_context = {'title': 'создание заказа'}
    fields = []
    # success_url — это куда пользователя будет перенаправлен после успешной отправки формы
    success_url = reverse_lazy('ordersapp:orders_list')  # . reverse_lazy перекидует нас на указанную страницу

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = ShopUser.get_items(self.request.user)

            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                    print('---------', basket_items[num].product.price)
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_summary()['get_total_cost'] == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    extra_context = {'title': 'изменение заказа'}
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:

                    form.initial['price'] = form.instance.product.price
                    print(form.initial)
            data['orderitems'] = formset
        return data

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            # оставил намеренно для тестов используй get_total_summary()['get_total_cost']
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    extra_context = {'title': 'удаление заказа'}
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DeleteView, self).dispatch(*args, **kwargs)


class OrderDetail(DetailView):
    extra_context = {'title': 'подробнее о заказе'}
    model = Order



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'просмотр заказа'
        return context

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)


def change_status_for_order(request, pk):
    """метод для изменения статуса заказа из FORMING на SENT_TO_PROCEED"""
    # change = get_object_or_404(Order, pk=pk)
    # change.statys = Order.SENT_TO_PROCEED
    change = Order.objects.filter(pk=pk).first()
    change.statys = Order.SENT_TO_PROCEED
    change.save()
    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketModel)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    # «sender» - класс модели, экземпляр которой будет сохранен.
    # «update_fields» - имена обновляемых полей;
    # «instance» - сам обновляемый объект
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(id=instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketModel)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
