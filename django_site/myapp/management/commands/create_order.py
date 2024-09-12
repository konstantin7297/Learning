from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from myapp.models import Order


class Command(BaseCommand):
    """ Тут пишется команда для вызова в формате: 'python manage.py create_order'. Ее так же можно увидеть через: 'python manage.py help'.
    Данная команда создает заказ. Такое описание всегда нужно делать для команды. """
    @transaction.atomic  # Делает функцию атомарной. Либо запрос выполнится полностью, либо что-то сломается и все изменения откатятся. Можно так: 'with transaction.atomic():'.
    def handle(self, *args, **options):  # Этот метод вызывается при запуске команды, тут ее логика.
        self.stdout.write("Creates order")  # Пишется в консоль в качестве ответа при запуске команды.

        user = User.objects.get(username="admin")  # Запрашивает пользователя.
        order = Order.objects.get_or_create(  # get_or_create - сам вызывает метод .save() после создания. Так что он не нужен. # noqa
            delivery_address="London Str. Taus.16",
            promocode="SALE123",
            user=user,  # Подается не id, а сама запись. Django сам найдет id и запишет его.
        )

        self.stdout.write(self.style.SUCCESS(f"Created order: {order}"))  # Пишется в консоль после успешного завершения команды.
