from django.contrib.auth.models import User, Permission, Group
from django.core.management import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    """ Тут пишется команда для вызова в формате: 'python manage.py update_user_rules'. Ее так же можно увидеть через: 'python manage.py help'.
    Данная команда добавляет права и группы прав к пользователю для доступа к некоторым элементам. Такое описание всегда нужно делать для команды. """
    @transaction.atomic  # Делает функцию атомарной. Либо запрос выполнится полностью, либо что-то сломается и все изменения откатятся. Можно так: 'with transaction.atomic():'.
    def handle(self, *args, **options):
        self.stdout.write("Updates rules")  # Пишется в консоль для ответа при запуске команды.

        user = User.objects.get(username="admin")  # Получаем пользователя.
        group, created = Group.objects.get_or_create(name="profile_manager")  # Создаем новую группу 'profile_manager'.

        permission_profile = Permission.objects.get(codename="view_profile")  # Получаем права 'view_profile'.
        permission_logentry = Permission.objects.get(codename="view_logentry")  # Получаем права 'view_logentry'.

        group.permissions.add(permission_profile)  # Добавляем группе новые права.
        user.groups.add(group)  # Добавляем группу с новыми правами пользователю.
        user.user_permissions.add(permission_logentry)  # Добавляем права напрямую пользователю, а не группе.

        group.save(update_fields=["permissions"])  # Сохранение данных. update_fields - оптимизирует запрос к БД только для изменяемых полей. # noqa
        user.save(update_fields=["user_permissions"])  # Сохранение данных. update_fields - оптимизирует запрос к БД только для изменяемых полей. # noqa

        self.stdout.write(self.style.SUCCESS("Successfully updates rules"))  # Пишется в консоль после успешного завершения команды.
