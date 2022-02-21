from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser
from django.urls import reverse
from adminapp.forms import ShopAdminUserEditForm, ShopAdminUserCreateForm, ShopAdminCategoryCreateForm,\
    ShopAdminCategoryUpdateForm, ShopAdminProductUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from ordersapp.models import Order, OrderItem
from django.forms import inlineformset_factory
from ordersapp.forms import OrderForm, OrderItemForm
from django.db import connection
from django.db.models import F

from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver


def my_db_profile(sender, type_queries, queries):
    """функция для ввыода иформации об запросе к БД(визуализацыя запроса)"""
    print(f'источник {sender}, тип запроса - {type_queries}, запросы----')
    [print(query) for query in queries if type_queries in query['sql']]


@receiver(pre_save, sender=ProductCategory)
def change_folder_is_active_in_product_(sender, instance, **kwargs):
    """функция для изменения поля is_active в Product при изменении поля is_active в ProductCategory,
    работает через сигналы"""
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        # my_db_profile(sender, 'UPDATE', connection.queries)  # -- если надо посмотреть команды в БД


# this functions is analog CBV UsersList
# def index(request):
#     all_users = ShopUser.objects.all()
#     content = {
#         'title': 'админка',
#         'all_users': all_users
#     }
#     return render(request, 'adminapp/index.html', context=content)


class UsersList(ListView):
    model = ShopUser
    template_name = 'adminapp/index.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = ShopUser.objects.filter(pk=pk).first()
    if request.method == 'POST':
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return HttpResponseRedirect(reverse('new_admin:index'))
    else:
        content = {
            'title': 'админка/удаление',
            'user': user,
        }
        return render(request, 'adminapp/user_delete.html', context=content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    # user = ShopUser.objects.filter(pk=pk)
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        update_form = ShopAdminUserEditForm(request.POST, request.FILES, instance=user)
        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('new_admin:index'))
    else:
        update_form = ShopAdminUserEditForm(instance=user)
        content = {
            'title': 'админка/редактирование',
            'update_form': update_form
        }
        return render(request, 'adminapp/user_update.html', context=content)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = ShopAdminUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('new_admin:index'))
    else:
        form = ShopAdminUserCreateForm()
        content = {
            'title': 'админка/создание_пользователя',
            'form': form
        }
        return render(request, 'adminapp/user_create.html', context=content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    all_categories = ProductCategory.objects.all()
    content = {
        'title': 'категории',
        'all_categories': all_categories
    }
    return render(request, 'adminapp/categories.html', context=content)


# this functions is analog CBV CategoriesCreateView
# @user_passes_test(lambda u: u.is_superuser)
# def categories_create(request):
#     if request.method == 'POST':
#         form = ShopAdminCategoryCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('new_admin:categories'))
#     else:
#         form = ShopAdminCategoryCreateForm()
#         content = {
#             'title': 'категории/создание',
#             'form': form
#         }
#         return render(request, 'adminapp/categories_create.html', context=content)


class CategoriesCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    success_url = reverse_lazy('new_admin:categories')
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

# this functions is analog CBV CategoryUpdateView
# @user_passes_test(lambda u: u.is_superuser)
# def categories_update(request, pk):
#     category = ProductCategory.objects.filter(pk=pk).first()
#     if request.method == 'POST':
#         form = ShopAdminCategoryUpdateForm(request.POST, request.FILES, instance=category)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('new_admin:categories'))
#     else:
#         form = ShopAdminCategoryUpdateForm(instance=category)
#         content = {
#             'title': 'категории/редактирование',
#             'form': form
#         }
#         return render(request, 'adminapp/categories_update.html', context=content)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    success_url = reverse_lazy('new_admin:categories')
    form_class = ShopAdminCategoryUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        """через переопределения этого метода, добиваемся применения скидки ко всем продуктам данной категории"""
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                # my_db_profile(self.__class__, 'UPDATE', connection.queries)    # -- если надо посмотреть команды в БД
        return super().form_valid(form)


@user_passes_test(lambda u: u.is_superuser)
def categories_delete(request, pk):
    category = ProductCategory.objects.filter(pk=pk).first()
    if request.method == 'POST':
        if category.is_active:
            category.is_active = False
            category.save()
        else:
            category.is_active = True
            category.save()
        return HttpResponseRedirect(reverse('new_admin:categories'))
    else:
        content = {
            'title': 'админка/категории/удаление',
            'categories': category,
        }
        return render(request, 'adminapp/category_delete.html', context=content)


# class CategoryDeleteView(DeleteView):
#     model = ProductCategory
#     template_name = 'adminapp/category_delete.html'
#     success_url = reverse_lazy('new_admin:categories')
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.is_active = False
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def product_list(request, pk):
    need_categories = ProductCategory.objects.filter(pk=pk).first()
    products = Product.objects.filter(category=pk)
    content = {
        'title': 'админка/категории/продукты',
        'category': need_categories,
        'object_list': products,
    }
    return render(request, 'adminapp/product_list.html', context=content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if request.method == 'POST':
        form = ShopAdminProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('new_admin:product_list', kwargs={"pk":product.category.pk}))
    else:
        form = ShopAdminProductUpdateForm(instance=product)
        content = {
            'title': 'категории/продукт/редактирование',
            'form': form,
            'link': product.category.pk
        }
        return render(request, 'adminapp/product_update.html', context=content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, category_pk):
    category = ProductCategory.objects.filter(pk=category_pk).first()
    if request.method == 'POST':
        form = ShopAdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('new_admin:product_list', kwargs={"pk": category.pk}))
    else:
        form = ShopAdminProductUpdateForm(initial={'category': category})
        content = {
            'title': 'продукт/создание',
            'form': form,
            'link': category.pk
        }
        return render(request, 'adminapp/product_update.html', context=content)
        # return HttpResponseRedirect(reverse('adminapp:product_create', kwargs={'category_pk': category_pk}))


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if request.method == 'POST':
        if product.is_active:
            product.is_active = False
            product.save()
        else:
            product.is_active = True
            product.save()
        return HttpResponseRedirect(reverse('adminapp:product_list', args=[product.category.pk]))
    else:
        content = {
            'title': 'категории/продукты/удаление',
            'product': product,
        }
        return render(request, 'adminapp/product_delete.html', context=content)


class OrderList(ListView):
    """По умолчанию Django будет искать шаблон с именем вида «<имя класса>_list.html"""
    model = Order
    extra_context = {'title': 'заказы'}

    def get_queryset(self):
        """по умолчанию данный метод выводит в форму все обьекты указзанной модели, но его можно переопределить чтоб
        он удовлетворял наши подребности"""
        item = Order.objects.filter(is_active=True)
        return item


class OrderStatusUpdate(UpdateView):
    model = Order
    fields = ['statys']
    extra_context = {'title': 'изменение статуса заказа'}
    success_url = reverse_lazy('new_admin:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data

