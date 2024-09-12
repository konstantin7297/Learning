import csv
from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin  # noqa
from django.db.models import QuerySet  # noqa
from django.db.models.options import Options  # noqa
from django.http import HttpRequest, HttpResponse  # noqa
from django.shortcuts import render, redirect  # noqa
from django.urls import path  # noqa

from .models import Product, ProductImage, Order, OrderImage
from .forms import CSVImport


@admin.action(description="Archiving")  # Имя параметра, которое будет отображаться в строке выбора для применения к списку записей.
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):  # noqa
    """ Функция добавляет действие для выбранного списка записей. В данном случае архивация всех выделенных записей одной кнопкой. """
    queryset.update(archived=True)


class ProductOrdersInline(admin.TabularInline):  # Добавляет раздел с указанной связью. 'admin.StackedInline' - немного другой визуал. # noqa
    """ Добавляет секцию на странице продукта, в которой показаны все указанные связанные объекты. В данном случае: 'Product.orders'. """
    model = Product.orders.through  # Эти объекты можно редактировать. through - загружает доп. таблицу, нужен для связи ManyToMany. # noqa


class ProductImagesInline(admin.TabularInline):  # Добавляет раздел с указанной связью. 'admin.StackedInline' - немного другой визуал. # noqa
    """ Добавляет секцию на странице продукта, в которой показаны все указанные связанные объекты. В данном случае: 'Product.images'. """
    model = ProductImage  # Эти объекты можно редактировать. through - загружает доп. таблицу, нужен для связи ManyToMany. # noqa


class OrderProductsInline(admin.StackedInline):  # Добавляет раздел с указанной связью. 'admin.TabularInline' - немного другой визуал. # noqa
    """ Добавляет секцию на странице продукта, в которой показаны все указанные связанные объекты. В данном случае: 'Order.products'. """
    model = Order.products.through  # Эти объекты можно редактировать. through - загружает доп. таблицу, нужен для связи ManyToMany. # noqa


class OrderImagesInline(admin.StackedInline):  # Добавляет раздел с указанной связью. 'admin.TabularInline' - немного другой визуал. # noqa
    """ Добавляет секцию на странице продукта, в которой показаны все указанные связанные объекты. В данном случае: 'Order.images'. """
    model = OrderImage  # Эти объекты можно редактировать. through - загружает доп. таблицу, нужен для связи ManyToMany. # noqa


class CSVMixin:
    """ Класс для работы с данными в .csv файлах. Можно настроить как скачивание, так и загрузку данных. """
    def export_csv(self, request: HttpRequest, queryset: QuerySet):  # Метод для скачивания данных в .csv файл. # noqa
        meta: Options = self.model._meta  # Возвращает данные модели БД. # noqa
        response = HttpResponse(content_type="text/csv")  # Создается ответ и указывается его тип данных.
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"  # attachment - значит скачать при запросе.
        field_names = [field.name for field in meta.fields]  # Отдает список названий полей таблицы БД.

        csv_writer = csv.writer(response)  # Создаем записывающий объект в файл response ответа.
        csv_writer.writerow(field_names)  # Загружаем поля в первой строке для именования столбиков.
        for obj in queryset:  # Пробегаемся по всем записям в БД и записываем их в файл.
            csv_writer.writerow([getattr(obj, field) for field in field_names])

        return response  # Возвращаем ответ: файл для скачивания. В Django response хранит данные как файл, так что response может быть файлом.

    export_csv.short_description = "Export as CSV"  # Описание кнопки на сайте для этого метода.


@admin.register(Product)  # Можно использовать 'admin.site.register(Product, ProductAdmin)'.
class ProductAdmin(admin.ModelAdmin):  # Регистрация модели БД для отображения по адресу: 'admin/'.
    """ Класс для описания модели таблицы БД для отображения на сайте в админке. """
    list_display = "pk", "name", "description_short", "price", "discount", "archived"  # Указывает поля, которые нужно отобразить в админке.
    list_display_links = "pk", "name"  # Указывает поля, на которые можно будет кликнуть для перехода на вкладку с доп. информацией по записи.
    ordering = "pk", "name"  # Указывает поля, по которым нужно сортировать выводимый результат. Указав '-pk' можно сделать обратную сортировку.
    search_fields = "name", "description"  # Добавляет строку поиска на сайте, в которой можно будет искать записи по данным из указанных в строке полей.
    actions = [mark_archived, CSVMixin.export_csv]  # Дополнительные опции в строке глобальных параметров, которые можно применить сразу к списку записей.
    inlines = [ProductOrdersInline, ProductImagesInline]  # Добавляет на сайте раздел со связанными объектами. В данном случае: 'Product.orders', 'Product.images' объекты.
    fieldsets = [  # Настройки доп. разделов. Формат: ('Имя раздела', {'настройки'}).
        ("More information", {  # Если раздел должен быть без имени, можно указать 'None'.
            "description": "This section give more information for product.",  # Описание для раздела, будет отображаться в разделе.
            "fields": ("description", "archived"),  # Указанные поля будут отображаться в разделе.
            "classes": ("collapse", "wide"),  # Доп. параметры визуального оформления раздела. # noqa
        }),  # collapse - раздел свернут по-умолчанию, можно развернуть нажатием. wide - значение поля будет с большим отступом. # noqa
        ("Images", {
            "description": "Section with preview, images",  # Секция показывает картинки продуктов.
            "fields": ("preview", "images"),  # Показывает 'preview', 'images' продуктов.
            "classes": ("collapse", "wide"),  # Доп. параметры визуального оформления раздела. # noqa
        }),  # collapse - раздел свернут по-умолчанию, можно развернуть нажатием. wide - значение поля будет с большим отступом. # noqa
    ]
    change_list_template = "admin/change_list.html"  # Измененная страница для админки с новой добавленной кнопкой от 'import_csv', 'get_urls' методов.

    def get_queryset(self, request):  # Функция для создания запроса к БД, который возвращаем все нужные данные для отображения.  # noqa
        """ Оптимизация загрузки: подгружаем orders, images и разом получаем все их данные одним запросом, что-бы отобразить все нужные связанные элементы для поля inlines. """
        return Product.objects.prefetch_related("orders", "images")  # noqa

    def description_short(self, obj: Product) -> str:  # Название функции указывается как поле для отображения в 'list_display'. # noqa
        """ Функция выводит вместо полного description - урезанный. Ее так же можно описать в файле: 'models.py' под декоратором '@property'. """
        if len(obj.description) <= 50:  # Настройка отображения нужных данных. Этот же параметр есть в модели таблицы.  # noqa
            return obj.description  # Описание записи будет сокращаться до 50 символов максимум.  # noqa
        return obj.description[:50] + "..."  # Возвращаются нужные данные, урезанные до 50 символов.  # noqa

    def import_csv(self, request: HttpRequest) -> HttpResponse:  # Функция для создания формы для загрузки данных из файла.
        if request.method == "GET":  # Если метод GET, отдаем форму для отправки файла.
            return render(request, 'admin/csv_form.html', context={"form": CSVImport()})

        form = CSVImport(request.POST, request.FILES)
        if not form.is_valid():  # Если форма заполнена не правильно, возвращаем ее с 400 ошибкой.
            return render(request, 'admin/csv_form.html', context={"form": CSVImport()}, status=400)

        csv_file = TextIOWrapper(form.files["csv_file"].file, encoding=request.encoding)  # Получает из bytes -> str.
        reader = DictReader(csv_file)
        Product.objects.bulk_create([Product(**row) for row in reader])  # Загружаем все записи в БД. # noqa
        self.message_user(request, "imported")  # Сообщение для пользователя.
        return redirect("..")  # Возвращаемся на предыдущий уровень страницы.

    def get_urls(self):  # Нужен для 'import_csv', добавляет ссылку на загрузку данных из файла.
        urls = super().get_urls()
        new_urls = [path(r'import-product-csv/', self.import_csv, name="import-product-csv")]
        return new_urls + urls  # Регистрируем новый path для импорта csv файла.


@admin.register(Order)  # Можно использовать 'admin.site.register(Order, OrderAdmin)'.
class OrderAdmin(admin.ModelAdmin):  # Регистрация модели БД для отображения по адресу: 'admin/'.
    """ Внутри можно описать ряд настроек для отображения на сайте админки. """
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"  # Указывает поля, которые нужно отобразить в админке. # noqa
    list_display_links = "delivery_address", "promocode"  # Указывает поля, на которые можно будет кликнуть для перехода на вкладку с доп. информацией по записи. # noqa
    ordering = "pk", "created_at"  # Указывает поля, по которым нужно сортировать выводимый результат. Указав '-pk' можно сделать обратную сортировку.
    search_fields = "delivery_address", "promocode"  # Добавляет строку поиска на сайте, в которой можно будет искать записи по данным из указанных в строке полей. # noqa
    actions = [CSVMixin.export_csv]  # Дополнительные опции в строке глобальных параметров, которые можно применить сразу к списку записей.
    inlines = [OrderProductsInline, OrderImagesInline]  # Добавляет на сайте раздел со связанными объектами. В данном случае: 'Order.products' объекты.
    fieldsets = [  # Настройки доп. разделов. Формат: ('Имя раздела', '{настройки}').
        ("More information", {  # Если раздел должен быть без имени, можно указать 'None'.
            "description": "This section give more information for order.",  # Описание для раздела, будет отображаться в разделе.
            "fields": ("user_verbose", "products"),  # Указанные поля будут отображаться в разделе.
            "classes": ("collapse", "wide"),  # Доп. параметры визуального оформления раздела. # noqa
        }),  # collapse - раздел свернут по-умолчанию, можно развернуть нажатием. wide - значение поля будет с большим отступом. # noqa
        ("Images", {
            "description": "Section with receipt, images",  # Секция показывает картинки продуктов.
            "fields": ("receipt", "images"),  # Показывает 'receipt', 'images' заказов.
            "classes": ("collapse", "wide"),  # Доп. параметры визуального оформления раздела. # noqa
        }),  # collapse - раздел свернут по-умолчанию, можно развернуть нажатием. wide - значение поля будет с большим отступом. # noqa
    ]
    change_list_template = "admin/change_list.html"  # Измененная страница для админки с новой добавленной кнопкой от 'import_csv', 'get_urls' методов.

    def get_queryset(self, request):  # Функция для создания запроса к БД, который возвращаем все нужные данные для отображения.  # noqa
        """ Оптимизация загрузки: подгружаем user, products, images и разом получаем все их данные одним запросом, что-бы отобразить все нужные связанные элементы для поля inlines. """
        return Order.objects.select_related("user").prefetch_related("products", "images")  # noqa

    def user_verbose(self, obj: Order) -> str:  # Название функции указывается как поле для отображения в 'list_display'. # noqa
        """ Функция выводит first_name пользователя или его username. Ее так же можно описать в файле: 'models.py' под декоратором '@property'. """
        return obj.user.first_name or obj.user.username  # Вернет имя, если оно есть, в противном случае username. # noqa

    def import_csv(self, request: HttpRequest) -> HttpResponse:  # Функция для создания формы для загрузки данных из файла.
        if request.method == "GET":  # Если метод GET, отдаем форму для отправки файла.
            return render(request, 'admin/csv_form.html', context={"form": CSVImport()})

        form = CSVImport(request.POST, request.FILES)
        if not form.is_valid():  # Если форма заполнена не правильно, возвращаем ее с 400 ошибкой.
            return render(request, 'admin/csv_form.html', context={"form": CSVImport()}, status=400)

        csv_file = TextIOWrapper(form.files["csv_file"].file, encoding=request.encoding)  # Получает из bytes -> str.
        reader = DictReader(csv_file)
        Order.objects.bulk_create([Order(**row) for row in reader])  # Загружаем все записи в БД. # noqa
        self.message_user(request, "imported")  # Сообщение для пользователя.
        return redirect("..")  # Возвращаемся на предыдущий уровень страницы.

    def get_urls(self):  # Нужен для 'import_csv', добавляет ссылку на загрузку данных из файла.
        urls = super().get_urls()
        new_urls = [path(r'import-order-csv/', self.import_csv, name="import-order-csv")]
        return new_urls + urls  # Регистрируем новый path для импорта csv файла.
