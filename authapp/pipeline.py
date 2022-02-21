# После авторизации пользователя мы делаем дополнительный запрос к ВКонтакте API, чтобы получить дополнительные данные.

from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'books', 'city', 'country',
                                                                 'photo_50')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return



    data = resp.json()['response'][0]

    print(data['books'])
    print(data['city'])
    print(data['country'])
    # print(data['has_mobile'])
    print('photo-------->', data['photo_50'])

    # with open('vk_about_me.txt', 'w') as f:
    #     f.write(data)

    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']


    user.shopuserprofile.about_me = f"любимые книги {data['books']}, родился в {data['country']['title']}, город {data['city']['title']}"

    # if data['bdate']:
    #     bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    #
    #     age = timezone.now().date().year - bdate.year
    #     if age < 18:
    #         user.delete()
    #         raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()