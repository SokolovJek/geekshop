from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserCreationForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from authapp.models import ShopUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required




def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    print('1')
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    print(login_form.is_valid())
    if request.method == 'POST' and login_form.is_valid():
        print('2')
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        print(user.is_active)
        if user and user.is_active:
            print('3111111')
            auth.login(request, user)
            print('3222222')
            if 'next' in request.POST.keys():
                print('3')
                return HttpResponseRedirect(request.POST['next'])
            else:
                print('4')
                return HttpResponseRedirect(reverse('main:index'))
    content = {
        'title': 'вход',
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', context=content)


def logout(request):
    # для выхода из системы достаточно просто удалить объект пользователя из request -> auth.logout(request)
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))


def register(request):
    if request.method == 'POST':
        reg = ShopUserCreationForm(request.POST, request.FILES)
        if reg.is_valid():
            user = reg.save()
            if send_verify_mail(user):
                print('отправка произошла')
                return render(request, 'authapp/first_auth.html')
            else:
                print('ошибка при отправке сообщения')
                return HttpResponseRedirect(reverse('authapp:login'))
        else:
            return render(request, 'authapp/erorr.html')
    else:
        reg = ShopUserCreationForm()
        content = {
            'title': 'register',
            'form': reg
        }
        return render(request, 'authapp/register.html', context=content)


# @transaction.atomic
# """старый контролер"""
# def edit(request):
#     title = 'редактирование'
#
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:edit'))
#     else:
#         edit_form = ShopUserEditForm(instance=request.user)
#
#     content = {'title': title, 'edit_form': edit_form}
#
#     return render(request, 'authapp/edit.html', content)


@login_required
@transaction.atomic
def edit(request):
    edit_form_user = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
    edit_form_user_profile = ShopUserProfileEditForm(request.POST, request.FILES, instance=request.user.shopuserprofile)
    if request.method == 'POST' and edit_form_user.is_valid() and edit_form_user_profile.is_valid():
        edit_form_user.save()
        return HttpResponseRedirect(reverse('mainapp:index'))

    content = {
        'title': 'Редактирование',
        'form_user': edit_form_user,
        'form_user_profile': edit_form_user_profile,
    }
    return render(request, 'authapp/edit.html', context=content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'подтвержение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале \
                {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == key and not user.is_activation_key_expired:
            print(2)
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'Exception error activation1  : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))





