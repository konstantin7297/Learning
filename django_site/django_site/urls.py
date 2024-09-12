"""django_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # noqa
from django.conf.urls.static import static  # noqa
from django.conf.urls.i18n import i18n_patterns  # noqa
from django.contrib.sitemaps.views import sitemap  # noqa
from django.conf import settings  # noqa
from django.urls import path, include  # noqa
from rest_framework.routers import DefaultRouter  # noqa
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView  # noqa

from myapp.views import page_not_fount, ProductModelViewSet  # Что бы импорт работал, надо отметить папку, в которой 'manage.py' как source root(синим цветом).  # noqa
from .sitemaps import sitemaps

handler404 = page_not_fount  # Это функция, которая вызывается при 404 ошибке. Нужно обязательно добавить перед использованием DEBUG=False, т.к. основная будет выключена.

# Настройка: REST Framework.
routers = DefaultRouter()  # Создает свою мини-API, где будут все переходы по данным от зарегистрированных функций и классов.
routers.register("products", ProductModelViewSet)  # Регистрирует класс. В итоге создается список url, где можно гулять по разным продуктам и изменять их.

# Настройка: все адреса приложения.
urlpatterns = [  # Тут расписаны все ссылки сайта, по которым можно переходить. Подключать можно модулями.
    path(r'admin/doc/', include('django.contrib.admindocs.urls')),  # Подключает документацию к проекту. Так же нужно подключить в файле: 'settings.py'. Желательно: 'pip install flake8 flake8-docstrings'.
    path(r'admin/', admin.site.urls),  # 'admin/' - префикс, который будет ставиться в формате: '127.0.0.1:8080/' + 'admin/'.
    path(r'api/schema/', SpectacularAPIView.as_view(), name="schema"),  # Основной класс для строения API на 'drf_spectacular'.
    path(r'api/schema/swagger/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),  # Документация Swagger.
    path(r'api/schema/redoc/', SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # Документация Redoc. # noqa
    path(r'api/', include(routers.urls)),  # Загружает все операции над ProductViewSet. Он хранит все ссылки, методы и т.д. В общем это API root для продуктов.
    path(r"sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemaps-view"),  # Подключает sitemap для сайта, что-бы поисковики легче находили и индексировали нужные страницы.
]

# Настройка: internationalization.
urlpatterns += i18n_patterns(  # Тут расписаны все ссылки сайта, которые нужно будет переводить в другую локализацию.
    path('myapp/', include('myapp.urls')),  # Импорт всех url myapp, которые в файле 'urls.py'. Это импорт всего модуля разом.
)

# Настройки только для DEBUG режима: Media, django-debug-toolbar профилирование.
if settings.DEBUG:  # Добавляем доступ к статическим файлам для приложения, но только в DEBUG режиме, что-бы можно было работать с файлами при разработке.
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))  # Подключаем медиа-статику, указав url и папку хранения для нее. Надо настроить в 'settings.py'.
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))  # Подключаем дефолт-статику, указав url и папку хранения для нее. Надо настроить в 'settings.py'.
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")),)  # Подключает адреса для 'django-debug-toolbar' профилирования.
