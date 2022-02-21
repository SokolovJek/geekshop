from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm, ShopUserCreationForm
from django import forms
from django.forms import HiddenInput


class ShopAdminUserEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ShopAdminUserCreateForm(ShopUserCreationForm):
    class Meta:
        model = ShopUser
        fields = ("username", "first_name", "age", "password1", "password2", "avatar", "email",)


class ShopAdminCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''


class ShopAdminCategoryUpdateForm(forms.ModelForm):
    """discount - добиваемся применения скидки ко всем продуктам данной категории в ../view.CategoryUpdateView()"""
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        fields = '__all__'
        # exclude = ()     # аналог


class ShopAdminProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

