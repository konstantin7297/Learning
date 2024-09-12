from django.core.management import BaseCommand
from django.db import transaction

from myapp.models import Product


class Command(BaseCommand):
    """ Тут пишется команда для вызова в формате: 'python manage.py create_products'. Ее так же можно увидеть через: 'python manage.py help'.
    Данная команда создает продукты. Такое описание всегда нужно делать для команды. """
    @transaction.atomic  # Делает функцию атомарной. Либо запрос выполнится полностью, либо что-то сломается и все изменения откатятся. Можно так: 'with transaction.atomic():'.
    def handle(self, *args, **options):
        self.stdout.write("Creates products")  # Пишется в консоль для ответа при запуске команды.

        for product_name in ["Laptop", "Desktop", "Smartphone"]:  # get_or_create - сам вызывает метод .save() после создания. Так что он не нужен. # noqa
            product, created = Product.objects.get_or_create(name=product_name)  # noqa
            self.stdout.write(f"Created product {product.name}")

        self.stdout.write(self.style.SUCCESS("Products created"))  # Пишется в консоль после успешного завершения команды.
