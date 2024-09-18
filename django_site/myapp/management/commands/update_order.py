from typing import Sequence  # noqa

from django.core.management import BaseCommand
from django.db import transaction

from myapp.models import Product, Order


class Command(BaseCommand):
    """ Тут пишется команда для вызова в формате: 'python manage.py update_order'. Ее так же можно увидеть через: 'python manage.py help'.
    Данная команда добавляет продукты к заказу. Такое описание всегда нужно делать для команды. """
    @transaction.atomic  # Делает функцию атомарной. Либо запрос выполнится полностью, либо что-то сломается и все изменения откатятся. Можно так: 'with transaction.atomic():'.
    def handle(self, *args, **options):
        self.stdout.write("Updates order")  # Пишется в консоль для ответа при запуске команды.

        order = Order.objects.first()  # Возвращает первую запись таблицы с заказами. # noqa

        if not order:  # Если записей нет, то завершаем работу команды.
            self.stdout.write("order not found")
            return

        for product in Product.objects.all():  # Запрашиваем все продукты. Product.objects.all(): Sequence[Product]. # noqa
            order.products.add(product)  # Добавляем все продукты к заказу. # noqa

        order.save()  # Сохраняем изменения, т.к. тут не используется метод 'get_or_create', который сам вызывает '.save()'.
        self.stdout.write(self.style.SUCCESS("Successfully added products"))  # Пишется в консоль после успешного завершения команды.
