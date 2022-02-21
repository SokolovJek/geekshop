from django.contrib import admin
from django.urls import path, include, re_path
import authapp.views as authapp
from django.conf import settings
from django.conf.urls.static import static


app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    re_path(r'^verify/(?P<email>.+)/(?P<key>\w+)/$', authapp.verify, name='verify'),
]