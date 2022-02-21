"""
Django settings for geekshop project.

Generated by 'django-admin startproject' using Django 2.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""





import os, json

"""настройки для сервера SERVER = True, developer = False"""
SERVER = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!803rpv)kc^8*p_b4k(rypzzgc#t&7zhe)&y$%u)#*&o1$7*ad'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',

    'mainapp',
    'authapp',
    'basketapp',
    'adminapp',
    'ordersapp',

    'rest_framework',
    # 'debug_toolbar',  # for debug_toolbar
    # 'template_profiler_panel',   # for debug_toolbar
    # 'django_extensions',   # for django-extensions
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddlewarape',     # for siege(login user)
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',   # for vk
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',          # for django-debug-toolbar
]

ROOT_URLCONF = 'geekshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'mainapp.context_processors.basket',                    # my context_processors.basket

                'social_django.context_processors.backends',          # for vk
                'social_django.context_processors.login_redirect',    # for vk


            ],
        },
    },
]

LOGIN_ERROR_URL = '/'    # for vk

WSGI_APPLICATION = 'geekshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'authapp.ShopUser'

# прописали для валидации is_authenticated пользователя, перед использованием приложения basketapp/views
LOGIN_URL = '/auth/login/'


# Настройка проекта Django для отправки почты
DOMAIN_NAME = 'http://localhost:8000'           # for send mail
EMAIL_HOST = 'localhost'                        # for send mail
EMAIL_PORT = '25'                               # for send mail
EMAIL_HOST_USER = 'django@geekshop.local'       # for send mail
EMAIL_HOST_PASSWORD = 'geekshop'                # for send mail
EMAIL_USE_SSL = False                           # for send mail
#
# # вариант python -m smtpd -n -c DebuggingServer localhost:25       !!!!   \|/
# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None

# вариант логирования сообщений почты в виде файлов вместо отправки
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'     # for send mail
EMAIL_FILE_PATH = 'tmp/email-messages/'                                # for send mail


# настройки аутентификации через вк
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',                    # for vk
    'social_core.backends.vk.VKOAuth2',                             # for vk
)


with open('geekshop/vk.json', 'r') as f:           # for vk
    VK = json.load(f)

SOCIAL_AUTH_VK_OAUTH2_KEY = VK['SOCIAL_AUTH_VK_OAUTH2_KEY']         # for vk
SOCIAL_AUTH_VK_OAUTH2_SECRET = VK['SOCIAL_AUTH_VK_OAUTH2_SECRET']  # for vk



SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True                   # for vk
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']                             # for vk



SOCIAL_AUTH_PIPELINE = (                                            # all piplene for login and auth with vk
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',

    'authapp.pipeline.save_user_profile',

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

#     Easy wrapper for sending a single message to a recipient list. All members
#     of the recipient list will see the other recipients in the 'To' field.


ACTIVATION_KEY_TTL = 48


# Для работы инструментов отладки на реальном сервере создаем callback-функцию show_toolbar()
if DEBUG:
   def show_toolbar(request):
       return True

   DEBUG_TOOLBAR_CONFIG = {
       'SHOW_TOOLBAR_CALLBACK': show_toolbar,
   }

DEBUG_TOOLBAR_PANELS = [                                    # for debug_toolbar
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
       'debug_toolbar.panels.profiling.ProfilingPanel',
       'template_profiler_panel.panels.template.TemplateProfilerPanel',
   ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')             # for debug_toolbar


LOW_CACHE = False  # for memcached
"""настройки для кэша"""
if SERVER:
    if os.name == 'posix':
       CACHE_MIDDLEWARE_ALIAS = 'default'
       CACHE_MIDDLEWARE_SECONDS = 120
       CACHE_MIDDLEWARE_KEY_PREFIX = 'geekshop'

       CACHES = {
           'default': {
               'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
               'LOCATION': '127.0.0.1:11211',
           }
       }

    LOW_CACHE = True
    # DATABASES['default'] = {
    #     'NAME': 'geekshop',
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'USER': 'django',
    #     'PASSWORD': 'geekbrains',
    #     'HOST': 'localhost'}              # - для виртуальной машины

    DATABASES['default'] = {
        'NAME': 'geekshop',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'postgres'}       # - для  сервера REG.ru