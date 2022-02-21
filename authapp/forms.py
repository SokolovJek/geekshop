from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import ShopUser, ShopUserProfile
from django.contrib.auth import get_user_model
from django.forms import HiddenInput
import random, hashlib


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        # model = ShopUser
        model = get_user_model()
        fields = ('username', 'password')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = f'form-control {field_name}'


class ShopUserCreationForm(UserCreationForm):
    class Meta:
        # model = ShopUser
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "age", "password1", "password2", "avatar", "email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self):
        """функция изменения логики метода save()"""
        user = super(ShopUserCreationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        # model = ShopUser
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "age", "password", "avatar", "email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserProfileEditForm(UserChangeForm):
    class Meta:
        # model = ShopUser
        model = ShopUserProfile
        fields = ('gender', 'tagline', 'about_me')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''