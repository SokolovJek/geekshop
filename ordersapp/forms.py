from django import forms
from ordersapp.models import Order, OrderItem
from mainapp.models import Product

class OrderForm(forms.ModelForm):
    """ Чтоб не сохранять в БД применяю (required=False), так как поле нужно для информации и jQUERY"""

    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_items().select_related('category')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
