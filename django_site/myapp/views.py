import logging
import random
from csv import DictWriter, DictReader
from io import TextIOWrapper

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Avg, Max, Min, Count, F, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.decorators import api_view, action  # noqa
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext, ngettext_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View

from .forms import ProductForm, ProductModelForm, LoginForm
from .models import Product, ProductImage, Order
from .serializers import ProductSerializer


log = logging.getLogger(__name__)  # Получаем логгер с именем файла. Уровни: DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL # noqa
log.info("Log: %s", 1)  # Так нужно форматировать логи. Через %s данные будут подставляться только при вызове лога. Если лог не нужен, он не будет обрабатываться процессором.


def page_not_fount(request, exception):  # Можно вызвать через: Http404()... # noqa
    """ Основная функция для отображения при ошибке 404. Она подключается в главном файле 'urls.py'. Функцию так же можно вызвать вручную. """
    return HttpResponseNotFound("<h1>Page not found</h1>")


def redirects_end(request: HttpRequest, val: int = 1):  # noqa
    """ Функция показывает, какие бывают редиректы и как их использовать. Они нужны для перенаправления. """
    if val == 1:  # Пример перенаправления на страницу Error 404.
        url = reverse("myapp:redirects_end", kwargs={"val": 1})  # Доп. вариант построения url. # noqa
        raise Http404()  # Эта страница устанавливается в основном файле 'urls.py'. Функция: 'page_not_fount'.

    elif val == 2:  # Пример перманентного перенаправления с 301 кодом. Мало функциональный вариант.
        url = reverse("/", args=(str("myapp:redirects_end"), 1))  # reverse - создает ссылку при запуске приложения.
        return HttpResponsePermanentRedirect(url)  # Создаст ссылку по типу: '/{redirects_end}/1'.

    elif val == 3:  # Пример временного перенаправления с 302 кодом. Мало функциональный вариант.
        url = reverse_lazy("/", args=(str("myapp:redirects_end"), 1))  # reverse_lazy - создает ссылку при вызове.
        return HttpResponseRedirect(url)  # Создаст ссылку по типу: '/{redirects_end}/1'.

    else:  # Пример универсального перенаправления с 301 или 302 кодом. Желательный вариант использования.
        url = reverse("/", args=(str("myapp:redirects_end"), 1))  # reverse и reverse_lazy описаны выше.
        return redirect(url, permanent=True)  # Можно и так: 'return redirect("/", permanent=False)'.  # redirect("..") - вернет на уровень выше...


def cookie_session_end(request: HttpRequest) -> HttpResponse:  # noqa
    """ Функция показывает, как можно работать с 'cookie' и 'session'. """
    if request.method == "GET":  # Пример чтения cookie и session.
        get_cookie = request.COOKIES.get("key", "default")  # key - ключ от cookie, default - значение по-умолчанию. # noqa
        get_session = request.session.get("key", "default")  # key - ключ от cookie, default - значение по-умолчанию. # noqa
        return HttpResponse(f"Cookie: '{get_cookie}' | Session: '{get_session}'")

    elif request.method == "POST":  # Пример установки cookie.
        response = HttpResponse("Cookie set")
        response.set_cookie("key", "value", max_age=3600)  # max-age - срок жизни cookie в секундах.
        return response

    else:  # Пример установки session.
        request.session["key"] = "value"  # noqa
        return HttpResponse("Session set")


def form_end(request: HttpRequest, mode: str = "html"):  # Для медиа-файлов нужно включить поддержку в файлах: 'settings.py', 'urls.py'. # noqa
    """ Функция для демонстрации работы с различными формами через функцию. """
    if mode == "html":  # Пример работы с HTML формой. Такая форма полностью написана прямо на странице в виде вёрстки.
        if request.method == "POST":  # Форма отправляется POST запросом, значит в этом методе обрабатываем полученные данные из формы.
            data = request.GET.dict()  # Вручную берем данные из формы.
            data["preview"] = request.FILES.get("preview")  # Берем и медиа-файлы из формы.
            data["images"] = request.FILES.get("images")  # Берем список медиа-файлов из формы.

            form = ProductForm(data=data)  # Подаем данные в форму для валидации. instance - объект, если нужно обновить его. # noqa
            if form.is_valid():  # Если валидация прошла успешно.
                product = Product.objects.create(**form.cleaned_data)  # Создаем новый продукт и сохраняем его. # noqa
                product.save()
                return reverse("myapp:form_end", kwargs={"mode": "html"})
        return render(request, "myapp/1-my_form.html", context={"form": None, "title": "HTML"})  # Если метод GET, значит отправляем пустую форму для заполнения.

    elif mode == "form":  # Пример работы с Django формой. Такая форма пишется в файле 'models.py' наследуя класс 'forms.Form'. # noqa
        if request.method == "POST":  # Форма отправляется POST запросом, значит в этом методе обрабатываем полученные данные из формы.
            form = ProductForm(request.POST, request.FILES)  # Подаем данные в форму для валидации.
            if form.is_valid():  # Если валидация прошла успешно.
                product = Product.objects.create(**form.cleaned_data)  # Создаем новый продукт и сохраняем его. # noqa
                product.save()
                return reverse("myapp:form_end", kwargs={"mode": "form"})
        return render(request, "myapp/1-my_form.html", context={"form": ProductForm(), "title": "Form"})  # Если метод GET, значит отправляем пустую форму для заполнения.

    elif mode == "modelform":  # Пример работы с Model формой. Такая форма пишется в файле 'models.py' наследуя класс 'forms.ModelForm'. # noqa
        if request.method == "POST":  # Форма отправляется POST запросом, значит в этом методе обрабатываем полученные данные из формы.
            form = ProductModelForm(request.POST, request.FILES)  # Подаем данные в форму для валидации.
            if form.is_valid():  # Если валидация прошла успешно.
                form.save()  # Т.к. форма сделана на основе модели таблицы БД. То можно сразу сохранять ее в БД.
                return reverse("myapp:form_end", kwargs={"mode": "modelform"})
        return render(request, "myapp/1-my_form.html", context={"form": ProductModelForm(), "title": "ModelForm"})  # Если метод GET, значит отправляем пустую форму для заполнения.

    else:  # Пример загрузки файлов через форму в отдельное место. Нужен header или enctype в форме: 'multipart/form-data' для загрузки файлов. # noqa
        if request.method == "POST" and request.FILES.get("myfile"):  # Если POST, значит получили форму с данными, и если есть объект 'myfile'. # noqa
            myfile = request.FILES["myfile"]  # Забираем файл в переменную. # noqa
            fs = FileSystemStorage()  # Помощник для работы с файлами из Django.
            filename = fs.save(myfile.name, myfile)  # Сохраняем файл, формат: 'save("Имя", "Файл")'. Возвращает имя файла. # noqa
            return reverse("myapp:form_end", kwargs={"mode": "modelform"})  # Перенаправляем пользователя куда надо.
        return render(request, 'myapp/1-my_form.html', context={"form": ProductModelForm(), "title": "Dont work form"})  # Если GET, отправляем пустую форму для заполнения.


def login_end(request: HttpRequest):  # Тут так же показан и logout. # noqa
    """ Функция для демонстрации ручной реализации авторизации и выхода с аккаунта. Важно создавать пользователя через User.objects.create_user(...) для кэширования пароля. """
    if request.method == "GET":  # Если пользователь запрашивает форму для заполнения.
        if request.user.is_authenticated:  # Если пользователь уже аутентифицирован. # noqa
            return reverse("myapp:redirects_end", kwargs={"val": 1})  # Перенаправляем его.
        return render(request, "myapp/1-my_form.html", context={"form": LoginForm(), "title": "Login form"})  # Отдаем пустую форму для аутентификации.

    user = authenticate(request=request, login=request.POST.get("login"), password=request.POST.get("password"))  # Вернет найденного пользователя или None.
    if user:  # Если данные верные и пользователь найден.
        login(request, user)  # Аутентифицируем его.  logout(request) - для выхода пользователя.
        return reverse("myapp:redirects_end", kwargs={"val": 1})  # Перенаправляем его.
    return render(request, "myapp/1-my_form.html", context={"form": LoginForm(), "title": "Login form", "error": "error"})  # Если данные не верные, говорим об ошибке.


@login_required  # Требует аутентификации для просмотра этой страницы.
@user_passes_test(lambda user: user.groups.filter(name="view_product").exists())  # Уникальная проверка с помощью функции. Например: есть у пользователя нужная группа.
@permission_required("myapp.view_product", raise_exception=True)  # Требует роль 'view_product'. raise_exception - выкл. перенаправление. Для группы не нужно 'myapp.'.
def rule_end(request: HttpRequest):  # request - обязательный параметр. # noqa
    """ Функция показывает, как можно работать с правами доступа и отрендерить страницы на функциях. На примере отображения списка продуктов. Доп. полезная информация:
    1) prefetch_related - Для ManyToMany связи. Делает отдельный поиск каждого объекта и объединяет их после в Python. Менее производительный.
    2) select_related - Для OneToOne связи и ForeignKey. Делает запрос на один объект и все. Более производительный. Можно юзать вместе с prefetch_related.
    3) get_object_or_404(Product, pk=1) - Вернет продукт с id = 1. Если его нет, то вернет страницу с ошибкой. """  # noqa
    context = {
        "title": "rule_end",
        "products": Product.objects.prefetch_related("images", "orders").all(),  # Вернет список продуктов с загруженными связями. # noqa
    }
    return render(  # Так можно отрендерить страницу с какими-то данными.
        request=request,  # Возвращаем данные самого запроса.
        template_name="myapp/2-rule.html",  # Путь до файла-шаблона HTML, который нужно отрендерить.
        context=context,  # Тут хранятся все переменные, которые нужно будет использовать в шаблонах Jinja2 на странице.
    )


class RuleView(View, LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin):  # Mixins описаны на функции 'rule_end'.
    """ Класс показывает, как можно работать с правами доступа и отрендерить страницы на классах. На примере отображения списка продуктов. Доп. полезная информация:
    1) prefetch_related - Для ManyToMany связи. Делает отдельный поиск каждого объекта и объединяет их после в Python. Менее производительный.
    2) select_related - Для OneToOne связи и ForeignKey. Делает запрос на один объект и все. Более производительный. Можно юзать вместе с prefetch_related.
    3) get_object_or_404(Product, pk=1) - Вернет продукт с id = 1. Если его нет, то вернет страницу с ошибкой. """  # noqa
    permission_required = "view_product"  # Указывается codename разрешения, которое необходимо для просмотра страницы. Может потребоваться: 'myapp.view_product'.

    def get(self, request: HttpRequest):  # request - обязательный параметр # noqa
        context = {
            "title": "RuleView",
            "products": Product.objects.prefetch_related("images", "orders").all(),  # Вернет список продуктов с загруженными связями. # noqa
        }
        return render(  # Так можно отрендерить страницу с какими-то данными.
            request=request,  # Возвращаем данные самого запроса.
            template_name="myapp/2-rule.html",  # Путь до файла-шаблона HTML, который нужно отрендерить.
            context=context,  # Тут хранятся все переменные, которые нужно будет использовать в шаблонах Jinja2 на странице.
        )

    def test_func(self):  # Функция проверки 'UserPassesTestMixin' группы у пользователя для посещения этой страницы.
        return self.request.user.groups.filter(name="view_product").exists()  # Если у пользователя есть искомая группа, то у него есть право на посещение страницы.


class CacheView(View):  # Кэш нужно предварительно включить в файле: 'settings.py'.
    """ Класс для демонстрации работы с кэшированием. Для функции можно повесить: '@cache_page(120)', где 120 - секунды жизни кэша. """
    @method_decorator(cache_page(120))  # Так кэшируются методы классов целиком. Нужен вспомогательный метод. Он же заменяет кэширование в 'urls.py'.
    def get(self, request: HttpRequest):  # request - обязательный параметр. # noqa
        get_cache = cache.get("my_context")  # Пробуем получить кэш вручную.
        if get_cache:  # Если есть кэш, его и отправляем.
            return render(request, "myapp/3-cache.html", context=get_cache)  # Отправляем кэшированные данные.

        context = {"first": random.randint(100, 1000), "second": random.randint(100, 1000), "third": random.randint(100, 1000)}
        cache.set("my_context", context, 300)  # Сохраняем кэш вручную: context на 300 секунд.
        return render(request, "myapp/3-cache.html", context=context)


class InternationalizationView(View):  # Нужны предварительные настройки в файле: 'settings.py'.
    """ Класс для примера работы с настройкой различных локализаций к проекту. Перевод на разные языки. """
    def get(self, request: HttpRequest):  # gettext - нужен для созданий локализаций на разные языки. gettext_lazy - выполняется только при обращении. # noqa
        """ Пример перевода основных значений из кода на другой язык. """
        message = gettext("Hello World!")  # Вносим значение в реестр, после чего оно будет переводиться на другие языки для отображения.
        return render(request, "myapp/4-internationalization.html", context={"value": message})

    def post(self, request: HttpRequest):  # noqa
        """ Пример перевода значений с разным количеством объектов. Настройка окончаний для них. """
        items_count = request.POST.get("count") or 0  # Берем количество объектов.
        items_line = ngettext_lazy(
            "one item",  # Надпись, если будет получен лишь 1 объект.
            "{count} items",  # Надпись, если будет получен 1+ объектов.
            items_count  # Фактически получаемое количество объектов. Переменная.
        )
        items_line = items_line.format(count=items_count)  # Подаем данные для определения текста с окончаниями.
        return render(request, "myapp/4-internationalization.html", context={"value": items_line})


class DatabaseView(View):  # Можно использовать сессии с ленивой загрузкой, что бы не загружать лишние данные.
    """ Класс, показывающий работу с БД и настройку оптимизированных запросов. В модели таблицы БД так же есть 'db_index', который ускоряет выполнение запросов. """
    @transaction.atomic  # Делает функцию атомарной, т.е. либо выполняется все, либо ничего. Так же можно использовать: 'with transaction.atomic():'.
    def get(self, request: HttpRequest) -> HttpResponse:  # noqa
        res = get_object_or_404(Product, pk=1)  # Вернет продукт с id=1, если его нет - вызовет перенаправление на 404 страницу. # noqa
        res, created = Order.objects.get_or_create(...)  # Создаст новый заказ или выдаст существующий. res - сам заказ, created - статус создания. Сам вызывает .save() # noqa
        Order.objects.prefetch_related("images")  # Оптимизация загрузки связей AnyToMany. # noqa
        Order.objects.select_related("user")  # Оптимизация загрузки связей OneToOne. # noqa
        Product.objects.values("pk", "name")  # Вернет список словарей с указанными полями. # noqa
        Product.objects.values_list("name", flat=True)  # values_list - вернет кортежи, flat=True - распакует данные в единый список. # noqa
        Product.objects.defer("description").all()  # defer - загружает указанные поля в ленивом режиме. Т.е. только при обращении к ним. # noqa
        Product.objects.only("name").all()  # only - загружает только указанные поля, а остальные нет. # noqa
        Product.objects.bulk_create([Product(...) for i in range(9)])  # Создание сразу списка продуктов. Сам вызывает .save() # noqa
        Product.objects.filter(name__contains="na").update(discount=10)  # Обновление записей. name__contains - содержит в поле name строку. Вернет количество обновлений. gte - min, lte - max, gt - доступен. # noqa
        Product.objects.aggregate(Avg("price"), Max("price"), Min("price"), Count("id"))  # Покажет агрегатные данные. avg=Avg("price") - вернет результат как поле avg. # noqa
        Product.objects.annotate(total=Count("orders__promocode", default=0))  # Так делается обращение к: 'Product.orders.promocode'. Обращение: 'products8.total'. # noqa
        Product.objects.update(price=F('price') * 1.10)  # F - обращение к полю самой модели для работы с ее же данными, не загружая их в память. # noqa
        Product.objects.filter(Q(price__lt=20) | Q(price__gt=100))  # Q - Строение более сложных запросов с условиями. Есть: '|' - или, '&' - и, '~Q()' - Ложь. # noqa
        return HttpResponse({"res": res})


class ProductTemplateView(TemplateView):  # TemplateView - Рендеринг страниц.
    """ Класс для рендеринга страниц. Работает аналогично функции, но многие вещи делает сам, поэтому желательно использовать такие классы. """
    template_name = "myapp/2-rule.html"  # Страница, которую нужно отрендерить. По-умолчанию: 'group_template.html'.
    template_name_suffix = "_template"  # Можно вручную указать template_name или суффикс для поиска шаблона. Не обязательное поле.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Загружаем все полученные из запроса данные в context.
        context["title"] = "ProductTemplateEnd"
        context["products"] = Product.objects.prefetch_related("images", "orders").all(),  # Вернет список продуктов с загруженными связями. # noqa
        return context


class ProductListView(ListView):  # ListView - Отображение на странице списка объектов.
    """ Класс для рендеринга страниц. Работает аналогично функции, но многие вещи делает сам, поэтому желательно использовать такие классы. """
    model = Product  # Модель нужной таблицы БД. Вместо model можно использовать более конкретный запрос через queryset для загрузки конкретных данных или связей.
    queryset = Product.objects.prefetch_related("images", "orders").filter(archived=False)  # НЕОБЗЯТЕЛЬНО. Запрос вернет отфильтрованные данные вместе со связями. Вместо 'model'. def get_queryset. # noqa
    context_object_name = "products"  # НЕОБЗЯТЕЛЬНО. Имя переменной в context, которое нужно вставить в эту модель таблицы на странице. По-умолчанию: 'object_list'.
    template_name = "myapp/2-rule.html"  # НЕОБЗЯТЕЛЬНО. Так можно указать полное имя шаблона вместо стандартного. По-умолчанию: 'myapp/product_list.html'.
    template_name_suffix = "_list"  # НЕОБЗЯТЕЛЬНО. Так можно указать суффикс шаблона. Значение п-умолчанию.
    # allow_empty = False  # Если список пуст - вернет 404 страницу.


class ProductDetailView(DetailView):  # DetailView - Отображение информации об конкретном объекте.
    """ Класс для рендеринга страниц. Работает аналогично функции, но многие вещи делает сам, поэтому желательно использовать такие классы. """
    model = Product  # Модель нужной таблицы БД. Вместо model можно использовать более конкретный запрос через queryset для загрузки конкретных данных или связей.
    queryset = Product.objects.prefetch_related("orders", "images").filter(archived=False)  # НЕОБЗЯТЕЛЬНО. Запрос вернет отфильтрованные данные вместе со связями. Вместо 'model'. # noqa
    context_object_name = "product"  # НЕОБЗЯТЕЛЬНО. Имя переменной в context, которое нужно вставить в эту модель таблицы на странице. По-умолчанию: 'object'.
    template_name = "myapp/5-product_details.html"  # НЕОБЗЯТЕЛЬНО. Так можно указать полное имя шаблона вместо стандартного. По-умолчанию: 'myapp/product_details.html'.
    template_name_suffix = "_details"  # НЕОБЗЯТЕЛЬНО. Так можно указать суффикс шаблона. Значение п-умолчанию.


class ProductCreateView(CreateView):  # CreateView - Отображение формы для создания объекта.
    """ Класс для рендеринга страниц. Работает аналогично функции, но многие вещи делает сам, поэтому желательно использовать такие классы. """
    model = Product  # Модель нужной таблицы БД.
    fields = "name", "price", "description", "discount", "preview", "images"  # Поля, которые нужно заполнить. Если нужна custom форма, можно указать: 'form_class' вместо 'fields'.
    form_class = ProductForm  # НЕОБЗЯТЕЛЬНО. Нужно, если требуется вместо стандартной ModelForm использовать свою. fields строка тогда удаляется. # noqa
    success_url = reverse_lazy("myapp:ProductTemplateView")  # Адрес перенаправления после успешной отправки формы. Доп. пример в 'ProductUpdateView'. # noqa
    template_name = "myapp/1-my_form.html"  # НЕОБЗЯТЕЛЬНО. По-умолчанию: 'myapp/product_form.html'.
    template_name_suffix = "_form"  # НЕОБЗЯТЕЛЬНО. Так можно указать суффикс шаблона. Значение по-умолчанию.

    def form_valid(self, form):  # Функция, которая вызывается при успешной валидации формы.
        return super().form_valid(form=form)  # Возвращает отработанный результат выполнения функции.


class ProductUpdateView(UpdateView):  # UpdateView - Отображение формы для обновления объекта.
    """ Класс для рендеринга страниц. Работает аналогично функции, но многие вещи делает сам, поэтому желательно использовать такие классы. """
    model = Product  # Модель нужной таблицы БД.
    fields = "price", "preview"  # Поля, которые нужно изменить. Если нужна custom форма, можно указать: 'form_class' вместо 'fields'.
    form_class = ProductModelForm  # НЕОБЗЯТЕЛЬНО. Нужно, если требуется вместо стандартной ModelForm использовать свою. fields строка тогда удаляется. # noqa
    template_name = "myapp/1-my_form.html"  # НЕОБЗЯТЕЛЬНО. По-умолчанию: 'myapp/product_form.html'.
    template_name_suffix = "_form"  # НЕОБЗЯТЕЛЬНО. Так можно указать суффикс шаблона. Значение по-умолчанию.

    def get_success_url(self):  # Вместо success_url, т.к. ссылка ведет на страницу, к которой нужно еще взять первичный ключ.
        return reverse("myapp:ProductDetailView", kwargs={"pk": self.object.pk})

    def form_valid(self, form):  # Кастомная обработка формы для загрузки списка отправленных картинок сразу. # noqa
        response = super().form_valid(form=form)
        for img in form.files.getlist("images"):  # Пробегаемся по всем отправленным картинкам и сохраняем их.
            ProductImage.objects.create(product=self.object, image=img)  # noqa
        return response


class ProductDeleteView(DeleteView):  # DeleteView - Отображение формы для удаления объекта.
    """ Класс для рендеринга страниц. Работает аналогично функции, но многие вещи делает сам, поэтому желательно использовать такие классы. """
    model = Product  # Модель нужной таблицы БД.
    success_url = reverse_lazy("myapp:ProductListView")  # Адрес перенаправления после успешной отправки формы. Доп. пример в 'ProductUpdateView'. # noqa
    template_name = "myapp/1-my_form.html"  # НЕОБЗЯТЕЛЬНО. По-умолчанию: 'myapp/product_confirm_delete.html'.
    template_name_suffix = "_confirm_delete"  # НЕОБЗЯТЕЛЬНО. Так можно указать суффикс шаблона. Значение по-умолчанию.

    def form_valid(self, form):  # Метод выполняет главное действие, если форма валидна. Пример: замена удаления записи на ее архивацию.
        success_url = self.get_success_url()  # Получаем ссылку для возвращения.
        self.object.archived = True  # Архивируем запись.
        self.object.save(update_fields=['archived'])  # Сохраняем изменения. update_field - делает запрос к БД более легким. # noqa
        return HttpResponseRedirect(success_url)  # Возвращаемся.


class ProductsAPIView(APIView):  # REST APIView - класс для стандартной обработки запросов. REST нужен для строения хорошего API. У него свои импорты.
    """ Класс для примера работы с REST Framework, у него можно легко включить Swagger.... Все как обычно, но немного другие импорты. Для функции нужен декоратор '@api_view()'. """  # noqa
    authentication_classes = [SessionAuthentication, BasicAuthentication]  # Настройка типов авторизации под конкретный класс APIView.
    permission_classes = [IsAuthenticated]  # Требует быть аутентифицированным для работы этого API.

    def get(self, request: Request) -> Response:  # noqa
        data = [product.name for product in Product.objects.all()]  # noqa
        return Response({"products": data})  # Вернет список имен продуктов.

    def post(self, request: Request) -> Response:  # Для отдачи большего кол-ва данных. # noqa
        serialized = ProductSerializer(Product.objects.all(), many=True)  # Обрабатывает список коллекций для отправки. # noqa
        return Response({"products": serialized.data})  # В 'data' хранятся ожидаемые данные для ответа.


class ProductsListGenericView(ListModelMixin, GenericAPIView):  # GenericAPIView - базовые классы в REST Framework, добавляет стандартные параметры: queryset...
    """ Пример работы с базовыми классами в REST Framework, они почти не отличаются от Django классов. """  # noqa
    queryset = Product.objects.all()  # noqa
    serializer_class = ProductSerializer

    def get(self, request: Request) -> Response:  # Вернет сериализованный список продуктов. # noqa
        return self.list(request)  # ListModelMixin - добавляет 'self.list()' для генерации списка элементов к отправке. # noqa


class ProductsListCreateAPIView(ListCreateAPIView):
    """ ListCreateAPIView - REST Framework поддерживает базовые классы(ListView, DetailView...), они используются почти аналогично и для тех же целей, но уже для API. """
    queryset = Product.objects.all()  # Собирает список продуктов. Так же на странице будет доступна форма для создания нового продукта. # noqa
    serializer_class = ProductSerializer  # Возвращает сериализованный список продуктов. # noqa


@extend_schema(description="desc")  # 'drf_spectacular' для улучшенной настройки API и ее документации. description - описание этой страницы API.
class ProductModelViewSet(ModelViewSet):  # Класс подключается в основном файле 'urls.py' добавляет целую API по разным операциям над моделью 'Product'.
    """ Создает страницу API для продуктов, на которой будут установлены различные методы взаимодействий: GET, PUT, POST, DELETE, OPTIONS... Так же можно настроить доп. фильтры, документацию и т.д. """
    queryset = Product.objects.prefetch_related("orders", "images").all()  # Возвращает список продуктов. # noqa
    serializer_class = ProductSerializer  # Сериализатор для запроса. Принимает данные в 'Python' формате и конвертирует в формат для отправки в 'JSON' и обратно. # noqa
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # Дополнительные фильтры для страницы API. Их нужно установить в файле: 'settings.py'.
    filterset_fields = ["name", "description", "price", "discount", "archived"]  # Добавляет поиск данных по выбранному полю. Нужен: 'DjangoFilterBackend'. # noqa
    search_fields = ["name", "description"]  # Добавляет поиск данных сразу по всем указанным полям. Нужен: 'SearchFilter'. # noqa
    ordering_fields = ["name", "price", "discount"]  # Добавляет сортировку по указанным полям для отображения данных. Нужен: 'OrderingFilter'. # noqa

    def list(self, *args, **kwargs):  # Просто переопределяется главный метод, возвращающий данные без изменений.
        return super().list(*args, **kwargs)  # Вернет список запрашиваемых данных с нужными надстройками.

    @extend_schema(summary="sum", responses={200: ProductSerializer, 404: OpenApiResponse(description="404 desc")})  # Дополнение 'drf_spectacular' для настройки API документации. Типа Swagger.
    def retrieve(self, *args, **kwargs):  # Этот метод API для продуктов настраивает страницу для возвращения 1 конкретного продукта.
        """ summary - краткое описание этого метода-url, responses - описание возвращаемых данных для этого метода-url. """  # noqa
        return super().retrieve(*args, **kwargs)  # Подключает URL типа: '/products/1' для получения информации об конкретном продукте.

    @action(methods=["GET"], detail=False)  # Добавляет новую кнопку на странице. detail=True - строит ссылку для конкретного объекта с учетом Primary key. # noqa
    def download_csv(self, request: Request):  # Функция добавляет возможность выгрузить данные через .csv файл. # noqa
        queryset = self.filter_queryset(self.get_queryset())  # Получаем данные от класса -> фильтруем их параметрами класса.
        fields = ["name", "description", "price", "discount"]  # Поля, которые нужно добавить в файл.
        queryset = queryset.only(*fields)  # Оптимизация запроса, загружаем только нужные поля.

        response = HttpResponse(content_type="text/csv")  # Создаем ответ сервера, в Django он уже является файлом, так что прямо его и можно отдавать для скачивания.
        response["Content-Disposition"] = f"attachment; filename=products.csv"  # attachment - скачивание файла.
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()  # Записывает fieldnames в первой строке.

        for product in queryset:  # Записываем все нужные данные в файл.
            writer.writerow({field: getattr(product, field) for field in fields})
        return response  # Отдаем файл для скачивания.

    @action(methods=["POST"], detail=False, parser_classes=[MultiPartParser])  # Добавляет новую кнопку на странице. detail=True - строит ссылку для конкретного объекта с учетом Primary key. # noqa
    def upload_csv(self, request: Request):  # Функция добавляет возможность загрузить данные из .csv файла. parser_classes - указывает, что загрузка будет из файла. # noqa
        csv_file = TextIOWrapper(request.FILES["file"].file, encoding=request.encoding)  # Получает из bytes -> str.
        reader = DictReader(csv_file)
        Product.objects.bulk_create([Product(**row) for row in reader])  # Загружаем все записи в БД. # noqa
        return Response({"ok": True})  # Возвращаем статус операции.


class ProductFeed(Feed):
    """ Класс показывает настройку страницы новостей, только несколько новых записей в кратком содержании. RSS лента - нужна для подписки на новости приложения. """
    title = "This is my title"  # Заголовок для ленты.
    description = "This is my description"  # Описано, как происходят обновления.
    link = reverse_lazy("myapp:ProductListView")  # Ссылка на список объектов.

    def items(self):  # Метод возвращает список объектов. # noqa
        return Product.objects.filter(archived=False).order_by("-pk")[:5]  # Будет возвращать последние 5 товаров. # noqa

    def item_title(self, item: Product):  # Добавляет заголовок для объектов.
        return item.name

    def item_description(self, item: Product):  # Добавляет краткое описание для объектов.
        return item.description[:100]

    def item_link(self, item: Product):  # Добавляет ссылку для деталей объектов. get_absolute_url прямо в модели таблицы заменит этот метод. # noqa
        return reverse("myapp:ProductDetailView", kwargs={"pk": item.pk})
