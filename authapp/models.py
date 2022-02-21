from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.utils.timezone import now

from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from geekshop.settings import ACTIVATION_KEY_TTL
from django.utils.functional import cached_property


from datetime import datetime


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    activation_key = models.CharField(verbose_name='код аутентификации', max_length=128, blank=True)
    is_activate_key_expires = models.DateTimeField(auto_now_add=True, null=True)

    def get_items(self):
        """метод для контролера заказа(OrderItemCreate)"""
        items = self.basket.all()
        return items

    @property
    def is_activation_key_expired(self):
        return now() - self.is_activate_key_expires > timedelta(hours=ACTIVATION_KEY_TTL)

    @cached_property
    def get_basket_user(self):
        """получаем корзину пользователя и кешируем ее для оптимизации"""
        return self.basket.all()

    def all_quantity(self):
        return sum(map(lambda a: a.quantity, self.get_basket_user))

    def all_sum(self):
        # вар1
        # c = []
        # a = self.basket.all()
        # for i in a:
        #     c.append(i.product.price * i.quantity)
        # return sum(c)
        # вар2
        # return sum(i.quantity * i.product.price for i in self.basket.all())
        # вар3
        return sum(map(lambda a: a.quantity * a.product.price, self.get_basket_user))


class ShopUserProfile(models.Model):
    MALE = 'М'
    FEMALE = 'Ж'
    GENDER_CHOICES = (
        (MALE, 'мужчина'),
        (FEMALE, 'женщина'),
    )
    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, unique=True, null=False, db_index=True)
    gender = models.CharField(verbose_name='пол', max_length=1, blank=True, choices=GENDER_CHOICES)
    tagline = models.CharField(verbose_name='увлечения', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='обо мне', max_length=518, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        """При работе со связью «один-к-одному» необходим механизм синхронных действий со связанной моделью. Мы
        используем декоратор @receiver, который при получении определенных сигналов вызывает задекорированный метод.
        В нашем случае сигналом является сохранение (post_save) объекта модели ShopUser (sender=ShopUser)."""
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()