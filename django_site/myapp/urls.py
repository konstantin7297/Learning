from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page  # noqa

from . import views

app_name = "myapp"  # Имя приложения, позволяет избежать ошибок с одинаковыми именами на разных приложениях, если их url совпадают. # noqa

urlpatterns = [  # Формат: Endpoint url | Функция для обработки запроса | Имя пути для возможности к нему обратиться.
    re_path(r'0/(?<val>[0-9])/', views.redirects_end, name="redirect_end"),  # redirect, re_path - путь на модуле 're'. Получает 'val' = 0-9
    path(r'1/', views.cookie_session_end, name="cookie_session_end"),  # Работа с 'cookie' и 'session'.
    path(r'2/<str:mode>/', views.form_end, name="form_end"),  # Работа с формами.
    path(r'3/', views.login_end, name="login_end"),  # Ручной Login / Logout пользователя.
    path(r'4/', views.rule_end, name="rule_end"),  # Работа с правами в функции.
    path(r'5/', views.RuleView.as_view(), name="RuleView"),  # Работа с правами в классе.
    path(r'6/', views.CacheView.as_view(), name="CacheView"),  # Работа с кэшем. Кэш прямо в path: 'cache_page(9)(views.CacheView.as_view())'.
    path(r'7/', views.InternationalizationView.as_view(), name="InternationalizationView"),  # Работа с локализацией: перевод на другие языки, изменение окончаний.
    path(r'8/', views.DatabaseView.as_view(), name="DatabaseView"),  # Работа с базой данных. Составление запросов и немного советов.

    path(r'9/', views.ProductTemplateView.as_view(), name="ProductTemplateView"),  # Базовый класс для рендеринга страницы.
    path(r'10/', views.ProductListView.as_view(), name="ProductListView"),  # Базовый класс для отображения списка объектов.
    path(r'11/<int:pk>/', views.ProductDetailView.as_view(), name="ProductDetailView"),  # Базовый класс для отображения деталей объекта.
    path(r'12/', views.ProductCreateView.as_view(), name="ProductCreateView"),  # Базовый класс для создания нового объекта.
    path(r'13/<int:pk>/', views.ProductUpdateView.as_view(), name="ProductUpdateView"),  # Базовый класс для редактирования объекта.
    path(r'14/<int:pk>/', views.ProductDeleteView.as_view(), name="ProductDeleteView"),  # Базовый класс для удаления объекта.

    path(r'15/', views.ProductsAPIView.as_view(), name="ProductsAPIView"),  # Базовый REST класс для отправки сериализованных данных. # noqa
    path(r'16/', views.ProductsListGenericView.as_view(), name="ProductsListGenericView"),  # Базовый REST класс с доп. параметрами для отправки сериализованных данных. # noqa
    path(r'17/', views.ProductsListCreateAPIView.as_view(), name="ProductsListCreateAPIView"),  # Базовый REST класс. Пример одного из серии классов для отправки сериализованных данных. # noqa

    path(r'18/', views.ProductFeed(), name="ProductFeed"),  # Класс для создания RSS ленты. С установкой плагина можно подписать на обновления и мониторить этот feed.
    path(r'19/', LoginView.as_view(  # Пример аутентификации пользователя в виде класса. Класс можно наследовать и дополнять при необходимости.
        template_name="myapp/1-my_form.html",  # Путь к файлу с формой для входа.
        redirect_authenticated_user=True,  # Перенаправляет уже аутентифицированных пользователей при попытке второй аутентификации.
    ), name="LoginView"),
    path(r'20/', LogoutView.as_view(  # Пример выхода из аутентификации пользователя в виде класса. Класс можно наследовать и дополнять при необходимости.
        template_name="myapp/1-my_form.html",  # Путь к файлу с формой для входа.
        next_page="9/",  # Страница, куда нужно отправить пользователя после аутентификации.
    ), name="LogoutView"),
]  # Регистрация всех endpoint'ов. Тут функциям обработки приписывается маршрут и параметры. # noqa
