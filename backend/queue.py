class Celery:
    """ Тут описан принцип создания очереди задач при помощи Celery + Redis + Flower. Из них Celery - сам инструмент, Redis - типа proxy, Flower - веб-интерфейс для мониторинга. """
    install = """
        Установка ПО для работы:
            1) docker pull redis - скачает контейнер redis, управлять им можно через консоль с помощью docker команд
            2) pip install celery[redis]==5.3.1 - скачает саму celery для работы, используется уже в коде, например tasks.py
            3) pip install flower - скачать веб-интерфейс для celery, запускается как celery только с модом flower

        Работа с docker, основные команды:
            1) docker run -p 6379:6379 --name my-redis -d redis | запускает контейнер с именем my-redis, -d - в фон. режиме # noqa
            2) docker ps - показать список запущенных контейнеров, -a - все контейнеры
            3) docker kill... закрыть контейнер
            4) docker stop... остановить контейнер
            5) docker remove... - удалить контейнер, только после остановки

        Работа с celery, консольные команды для некоторых случаев:
            1) celery -A tasks worker --loglevel=warning - запускает  celery файла tasks в режиме worker с логами
            2) celery -A tasks control revoke <task_id> - отменяет задачу
            3) ps aux|grep 'celery worker' - показать все процессы celery
            4) pkill -f "celery worker" - закрывает все celery процессы

        Пример запуска и закрытия докера вместе с приложением прямо в коде(Только для тестов годится.):
            try:
                cnt = subprocess.Popen(shlex.split('docker run -p 6379:6379 --name my-redis -d redis'), stdout=subprocess.PIPE)
                app.run() # или celery: celery_client.worker_main(['worker']) # 2 приложения сразу не запускаются
            finally:
                name_close_cnt = subprocess.Popen(shlex.split(f'docker stop {cnt.communicate()[0].decode()}'), stdout=subprocess.PIPE)
                subprocess.Popen(shlex.split(f'docker remove {name_close_cnt.communicate()[0].decode()}'))
    """  # noqa

    info = """
        Пример реализации работы, режимы работы:
            1) worker - включается для работы с задачами в реальном времени (получил задачу - сразу выполняет)
            2) beat - включается для работы с периодическими задачами (получил задачу - выполнил по графику в указанное время или с интервалом времени) # noqa
            3) flower - включается для запуска веб-интерфейса, в котором можно мониторить процесс работы celery и влиять на него, стандарт адрес: http://localhost:5555

        Основные методы задач:
            1) func_x2.delay(3) - запуск функции через celery с поданными аргументами
            2) func_x2.apply_async(3) - запуск списка функций для одновременного выполнения, то же, что и .delay(), но для group(), chain()...
            3) func_x2.s(3) - передает аргументы функции, нужен когда требуется передать вызов задачи другому процессу или в качестве аргумента другой
                функции, например: func_x2.s(2).delay(3) = func_x2.delay(5). Подходит для подачи аргументов перед запуском в apply_async или add_periodic_task

        Основные методы результатов (на примере: result = group(func_x2.s(2), func_x3.s(3)).apply_async()):
            1) result.get() - получить результат работы объекта (в случае списка задач выведет список их ответов)
            2) result.id - отдаст id группы задач для последующего мониторинга и т.д.
            3) result.ready() - показывает, завершена ли задача
            4) result.successful() - показывает, успешно ли завершена задача
            5) result.failed() - показывает, если задача завершена безуспешно
            6) result.result - показывает информацию об ошибке, если она возникла при выполнении
            7) result.collect() - позволяет итерироваться по результатам, например когда задача возвращает список
            8) result.children - список детей # не понятно
            9) result.completed_count() - количество выполненных задач

        Получение результата по id задачи:
            result = celery_client.GroupResult.restore(group_id) - Возвращает объект result по id
    """  # noqa

    from celery import Celery, group, chain  # noqa
    from celery.schedules import crontab  # noqa
    import os

    celery_client = Celery(
        f'{os.path.basename(__file__)[:-3]}',  # название приложения для задач, указывается имя файла без расширения # noqa
        broker='redis://localhost:6379/0',  # URL брокера сообщений, он хранит задачи и отдает очереди # noqa
        backend='redis://localhost:6379/0'  # URL хранилища результатов; можно указать URL брокера # noqa
    )

    @celery_client.task
    def func_x2(num: int) -> int:  # noqa
        """ Функция для примера задачи: на нее ставится декоратор задачи для доступа к celery методам """
        print(f'func_x2: {num} * 2 = {num * 2}')
        return num * 2

    @celery_client.task
    def func_x3(num: int) -> int:  # noqa
        """ Функция для примера задачи: на нее ставится декоратор задачи для доступа к celery методам """
        print(f'func_x3: {num} * 3 = {num * 3}')
        return num * 3

    @celery_client.on_after_configure.connect
    def periodic_tasks(sender, **kwargs):  # noqa
        """ Функция для примера планирования задач: на ней фиксированный декоратор и аргументы, запускается через beat mode """  # noqa
        sender.add_periodic_task(60, func_x2.s(4))  # задача выполняется каждые 60 сек # noqa
        sender.add_periodic_task(crontab(hour=7, minute=30, day_of_week=1), func_x2.s(4))  # каждый понедельник в 7:30 по UTC(по умолчанию) # noqa

    # Эта часть делается уже в другом файле, импортируется по типу: from file import func_x2, func_x3 и from celery import group... # noqa
    tasks = group(func_x2.s(2), func_x3.s(3))  # Группа задач нужна для одновременного выполнения нескольких задач # noqa
    tasks = chain(func_x2.s(2), func_x3.s())  # Цепочка задач нужна рабоает так: результат первой передается во вторую и т.д. # noqa
    result = tasks.apply_async()  # запускает список задач в работу # noqa
    result.save()  # хз зачем # noqa
    result.get()  # получить результат: group(...) -> [4, 9] | chain(...) -> 12 # noqa
