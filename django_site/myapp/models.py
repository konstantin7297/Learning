from django.contrib.auth.models import User
from django.db import models


def path_to_preview(instance: "Product", filename: str) -> str:
    """ Функция, которая будет генерировать путь для хранения изображений 'preview' поля из модели 'Product'. """
    return f"products/product_{instance.pk}/preview/{filename}"  # Product.pk - свой же id. # noqa


def path_to_img1(instance: "ProductImage", filename: str) -> str:
    """ Функция, которая будет генерировать путь для хранения изображений 'images' поля из модели 'Product'. """
    return f"products/product_{instance.product.pk}/images/{filename}"  # ProductImage.product.pk - связь. # noqa


def path_to_receipt(instance: "Order", filename: str) -> str:
    """ Функция, которая будет генерировать путь для хранения изображений 'receipt' поля из модели 'Order'. """
    return f"orders/order_{instance.pk}/receipt/{filename}"  # Order.pk - свой же id. # noqa


def path_to_img2(instance: "OrderImage", filename: str) -> str:
    """ Функция, которая будет генерировать путь для хранения изображений 'images' поля из модели 'Order'. """
    return f"orders/order_{instance.order.pk}/images/{filename}"  # OrderImage.order.pk - связь. # noqa


class Product(models.Model):
    """ Таблица для продуктов. В Django поле 'id' создается автоматически. Эта строка будет в документации. Ссылка для документации на заказы: :model:`myapp.Order` """  # noqa
    class Meta:  # Дополнительные параметры для работы модели таблицы БД: сортировка полей, имя таблицы, разрешения и т.д.
        ordering = ['name', 'price']  # Поля, по которым будет сортироваться отображаемый результат. '-name' - в обратном порядке.
        verbose_name = "product"  # Имя таблицы в единственном числе для отображения.
        verbose_name_plural = "products"  # Имя таблицы в множественном числе для отображения.
        index_together = ['name', 'description']  # Поля, которые должны быть проиндексированными вместе.
        permissions = [("can_deliver_pizzas", "Can deliver pizzas")]  # Дополнительные разрешения для таблицы.
        constraints = []  # Ограничения таблицы. Тут проверки условий, уникальность значений и другие параметры, например: 'models.CheckConstraint()'. # noqa
        db_table = "tech_products"  # Полностью заменяет имя таблицы для обращения к ней.
        db_table_comment = "table with products"  # Комментарий для всей таблицы.

    name = models.CharField(max_length=100, db_index=True)  # Строковое поле. max_length - максимальная длина значения в поле. db_index - индекс для ускорения поиска по этому полю. # noqa
    description = models.TextField(null=False, blank=True, db_index=True)  # null - поле может быть пустым. black - поле может быть равным: "". # noqa
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)  # max_digits - кол-во цифр в числе, decimal_places - кол-во цифр после запятой.
    discount = models.SmallIntegerField(default=0)  # Небольшое число. default - значение по-умолчанию. # noqa
    created_at = models.DateTimeField(auto_now_add=True)  # При создании автоматически сохраняет дату создания.
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=path_to_preview)  # Поле для работы с изображениями. Содержит: preview.url - путь до картинки, preview.name - имя картинки. # noqa

    def __str__(self) -> str:  # Метод позволяет в админке выводить вместо названия таблицы что-то конкретное.
        return f"Product: #{self.name}"  # Заголовок на странице объекта будет по такому шаблону.

    @property  # Позволяет установить фильтр для отображения параметров в админке и не только. Больше информации в 'admin.py'.
    def description_short(self) -> str:  # Если метод нужен только в админке, его лучше объявить в 'admin.py'.
        """ Функция выводит вместо полного description - урезанный. """
        if len(self.description) <= 50:  # Настройка отображения нужных данных. Этот же параметр есть в модели таблицы.  # noqa
            return self.description  # Описание записи будет сокращаться до 50 символов максимум.  # noqa
        return self.description[:50] + "..."  # Возвращаются нужные данные, урезанные до 50 символов.  # noqa


class ProductImage(models.Model):
    """ Таблица для изображений продуктов. Содержит связи ManyToOne к таблице 'Product'. Эта строка будет в документации. Ссылка для документации на заказы: :model:`myapp.Order` """  # noqa
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")  # Связь с таблицей: 'Product.images', при удалении Product - удалится и images.
    image = models.ImageField(upload_to=path_to_img1)  # Сам объект картинки. upload_to - место хранения картинки. Содержит: image.url - путь до картинки, image.name - имя картинки. # noqa
    description = models.CharField(max_length=200, null=False, blank=True)  # Описание для картинки.


class Order(models.Model):
    """ Таблица для заказов. В Django поле 'id' создается автоматически. Эта строка будет в документации. Ссылка для документации на заказы: :model:`myapp.Product` """  # noqa
    class Meta:  # Дополнительные параметры для работы модели таблицы БД: сортировка полей, имя таблицы, разрешения и т.д.
        ordering = ['delivery_address', 'promocode']  # Поля, по которым будет сортироваться отображаемый результат. '-promocode' - в обратном порядке. # noqa
        verbose_name = "order"  # Имя таблицы в единственном числе для отображения.
        verbose_name_plural = "orders"  # Имя таблицы в множественном числе для отображения.
        index_together = ['delivery_address', 'promocode']  # Поля, которые должны быть проиндексированными вместе. # noqa
        permissions = [("can_deliver_pizzas", "Can deliver pizzas")]  # Дополнительные разрешения для таблицы.
        constraints = []  # Ограничения таблицы. Тут проверки условий, уникальность значений и другие параметры, например: 'models.CheckConstraint()'. # noqa
        db_table = "tech_orders"  # Полностью заменяет имя таблицы для обращения к ней.
        db_table_comment = "table with orders"  # Комментарий для всей таблицы.

    delivery_address = models.TextField(null=True, blank=True)  # null - поле может быть пустым. black - поле может быть равным: "". # noqa
    promocode = models.CharField(max_length=20, null=False, blank=True)  # Строковое поле. max_length - максимальная длина значения в поле. # noqa
    created_at = models.DateTimeField(auto_now_add=True)  # При создании автоматически сохраняет дату создания.
    user = models.ForeignKey(User, on_delete=models.PROTECT)  # Первичный ключ, при удалении родителя выдаст ошибку: 'Order' запрещает удалять родителя.
    products = models.ManyToManyField(Product, related_name="orders")  # Связь ManyToMany к 'Product.orders'.
    receipt = models.FileField(null=True, upload_to=path_to_receipt)  # Поля для фото чеков. Они хранятся: 'MEDIA_ROOT/orders/receipts/'.

    def __str__(self) -> str:  # Метод позволяет в админке выводить вместо названия таблицы что-то конкретное.
        return f"Order: #{self.delivery_address}"  # Заголовок на странице объекта будет по такому шаблону.

    @property  # Позволяет установить фильтр для отображения параметров в админке и не только. Больше информации в 'admin.py'.
    def delivery_address_short(self) -> str:  # Если метод нужен только в админке, его лучше объявить в 'admin.py'.
        """ Функция выводит вместо полного delivery_address - урезанный. """
        if len(self.delivery_address) <= 50:  # Настройка отображения нужных данных. Этот же параметр есть в модели таблицы.  # noqa
            return self.delivery_address  # Адрес записи будет сокращаться до 50 символов максимум.  # noqa
        return self.delivery_address[:50] + "..."  # Возвращаются нужные данные, урезанные до 50 символов.  # noqa


class OrderImage(models.Model):
    """ Таблица для изображений продуктов. Содержит связи ManyToOne к таблице 'Order'. Эта строка будет в документации. Ссылка для документации на заказы: :model:`myapp.Product` """  # noqa
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="images")  # Связь с таблицей: 'Order.images', при удалении Order - удалится и images.
    image = models.ImageField(upload_to=path_to_img2)  # Сам объект картинки. upload_to - место хранения картинки. Содержит: image.url - путь до картинки, image.name - имя картинки. # noqa
    description = models.CharField(max_length=200, null=False, blank=True)  # Описание для картинки.
