class LoggingLog:
    """ Тут описан принцип работы с модулем logging, это библиотека по умолчанию для логирования кода. """
    @staticmethod
    def small():  # noqa
        """ Тут мелкий вариант реализации самого простого logger'а. Настраивается с помощью доп. методов и классов. """
        import logging  # Уровни: DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL # noqa

        logging.basicConfig(level=logging.INFO, format="%(asctime)s| %(message)s", datefmt="%m-%d-%Y %I:%M:%S %p", encoding="utf-8")  # noqa
        logger = logging.getLogger("logger")  # %()s - выводит переменную внутри. При этом форматирует строку, только в момент ее вызова. # noqa

    @staticmethod
    def big():  # noqa
        """ Тут пример крупной реализации, которая подойдет для полноценного проекта. """
        import logging.config  # noqa
        import sys

        class FilesHandler(logging.Handler):  # noqa
            """ Кастомный класс обработчика для записи в файл """

            def __init__(self, file='calc.log', mode='a'):
                """ Инициализация кастомного обработчика """  # noqa
                super().__init__()
                self.file = file
                self.mode = mode

            def emit(self, record: logging.LogRecord) -> None:  # noqa
                """ Метод, который записывает логи в файл """
                message = self.format(record)
                with open(self.file, self.mode) as file:
                    file.write(message + '\n')

        class MyFilter(logging.Filter):  # noqa
            """ Кастомный класс фильтра для логгера """  # noqa

            def __init__(self):
                super().__init__()
                self.ascii_syms = string.printable  # noqa

            def filter(self, record: logging.LogRecord) -> bool:  # noqa
                """ Метод, который возвращает ответ, прошел ли текст фильтр или нет """
                for sym in record.msg:
                    if sym not in self.ascii_syms:
                        return False
                return True

        logging.config.dictConfig({  # noqa
            'version': 1,  # Версия логирования.
            'disable_existing_loggers': False,  # Нужно ли отключить уже существующие логгеры. # noqa
            'filters': {'ascii': {'()': MyFilter}},  # Фильтр ascii, который проверяет, что сообщение состоит из ascii символов.
            'formatters': {  # Форматы вывода сообщений.
                'base': {'format': '%(name)s | %(levelname)s | %(message)s'},  # %()s - выводит переменную внутри. При этом форматирует строку, только в момент ее вызова. # noqa
                'task2': {'class': 'logging.Formatter', 'fmt': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'},  # name - имя логгера, lineno - строка ошибки. # noqa
            },
            'handlers': {  # Обработчики сообщений.
                'console': {'class': 'logging.StreamHandler', 'filters': ['ascii'], 'level': 'INFO', 'formatter': 'task2', 'stream': sys.stdout},  # Обработчик для консоли.
                'files': {'()': FilesHandler, 'filters': ['ascii'], 'level': 'DEBUG', 'formatter': 'base'},  # Custom обработчик для записи в файл.
                "files2": {'class': "logging.handlers.RotatingFileHandler", "filename": "log.txt", "maxBytes": 1024, "backupCount": 3, "formatter": "task2"},  # Обработчик для ротации файлов по размеру.
                'utils_time': {'class': 'logging.handlers.TimedRotatingFileHandler', 'when': 'H', 'interval': 10, 'filename': 'utils.log', 'filters': ['ascii'], 'level': 'INFO', 'formatter': 'base'},  # По времени.
                'GET_HTTP': {'class': 'logging.handlers.HTTPHandler', 'level': 'DEBUG', 'formatter': 'base', 'host': '127.0.0.1:3000', 'url': '/getlog', 'method': 'POST'},  # Обработчик для endpoint.
                'PRINT_HTTP': {'class': 'logging.handlers.HTTPHandler', 'level': 'DEBUG', 'formatter': 'base', 'host': '127.0.0.1:3000', 'url': '/printlog', 'method': 'POST'},
            },
            'loggers': {
                'app_logger': {'level': 'INFO', 'handlers': ['console', 'files', 'GET_HTTP', 'PRINT_HTTP'], 'propagate': False},  # propagate - наследование логов от root логера. # noqa
                'utils_logger': {'level': 'INFO', 'handlers': ['console', 'files', 'utils_time', 'GET_HTTP', 'PRINT_HTTP'], 'propagate': False},
            }
        })  # Загрузка настроек логгеров. # noqa
        app_logger = logging.getLogger('app_logger')  # noqa
        utils_logger = logging.getLogger('utils_logger')  # noqa


class LoguruLog:
    """ Дополнительный logger, может работать на config от logging модуля. """
    from loguru import logger  # noqa

    logger.add(
        "logs/log.log",  # название файла с логами # noqa
        rotation="1 weak",
        # Записывает логи в новый файл каждую неделю (разделяя так логи по недельным файлам) # noqa
        compression="zip",  # Формат сжатия файлов # noqa
        level="INFO",
        format="{time} {level} {message}",
        backtrace=True,  # в случае ошибок, будет вызван traceback для получения инфы # noqa
        diagnose=True,  # в случае ошибок, будет вызван traceback для получения инфы # noqa
        serialize=True  # преобразование событий в json # noqa
    )

    @logger.catch  # равен logger.exeption, отвечает за логирование, если ловит ошибку - фиксирует ее # noqa
    def my_func():  # noqa
        logger.info('INFO-message')  # классическое логгирование # noqa
        return "Yes, i'm your func"


class StructloggerLog:
    """ Еще одно дополнительное логирование. """
    from structlog.stdlib import LoggerFactory  # noqa
    from flask import Flask, request, g  # noqa
    import datetime  # noqa
    import structlog  # noqa
    import logging  # noqa
    import sys

    app = Flask(__name__)

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)  # noqa
    structured_log = structlog.get_logger()

    def timestamper(_, __, event_dict):  # Получает событие и добавляет по нему доп. ключ - активного времени # noqa
        event_dict['time'] = datetime.datetime.now().isoformat()  # noqa
        return event_dict

    structlog.configure(
        processors=[timestamper, structlog.processors.JSONRenderer()],
        # События в журнал будут попадать в формате json # noqa
        logger_factory=LoggerFactory()  # Для синхронизации с базовым логгером # noqa
    )

    @app.before_request
    def before_request():  # Тут в наш лог-словарь добавляется инфа по запросу в приложение # noqa
        method = request.method  # noqa
        user_agent = request.user_agent  # noqa
        log = structured_log.bind(method=method, user_agent=user_agent)  # noqa
        g.log = log  # noqa

    @app.route('/one')
    def one():  # noqa
        g.log.msg('route one')  # noqa
        return 'one', 200


class FlaskProfiler:
    """ Тут описано профилирование(сбор статистики) с помощью библиотеки 'flask_profiler'. Веб интерфейс находится на: /flask-profiler/ """
    from flask import Flask  # noqa
    import flask_profiler  # noqa
    import flask  # noqa
    import decimal  # noqa

    app = Flask(__name__)
    app.config['flask_profiler'] = {  # config для flask_profile, тут обязательные параметры # noqa
        "enabled": True,  # Вкл, можно включать при дебаге: app.config['DEBUG'] # noqa
        "storage": {
            # на классическом sqlite есть баг с синхронным вызовом cursor, так что лучше alchemy # noqa
            "engine": "sqlalchemy",
            "db_url": "sqlite:///flask_profiler.db"
        },
        "basicAuth": {  # параметры авторизации в веб-интерфейсе # noqa
            "enabled": True,
            "username": "admin",
            "password": "admin"
        }
    }

    flask_profiler.init_app(app)

    class NewEncoder(flask.json.JSONEncoder):  # noqa
        """ Дописанный класс, который фиксит ошибку типов при сериализации flask'ом: 
        библиотека flask_profiler использует Decimal для работы с float числами,
        этот класс в случае получения Decimal объекта преобразует его в строку, благодаря чему
        в последующей обработке flask может сериализовать str формат (ошибка исчезнет, ведь Decimel 
        он не может сериализовать) """  # noqa

        def default(self, o):
            if isinstance(o, decimal.Decimal):  # noqa
                return str(o)
            return super(NewEncoder, self).default(o)  # noqa

    app.json_encoder = NewEncoder

    @app.route('/one', methods=['GET'])
    @flask_profiler.profile()
    def one():  # noqa
        return 'one', 200


class WerkzeugProfiler:
    """ Тут описано базовое профилирование на 'werkzeug_profiler'. Особенность: слишком много информации. """
    from werkzeug.middleware.profiler import ProfilerMiddleware  # noqa
    from flask import Flask  # noqa

    app = Flask(__name__)
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='..')
    # Всего пара строчек, все уже работает, но информацию придется искать в куче не нужной. Файлы можно читать
    # через инструменты чтения файлов .prof


class PrometheusGraphanaProfiler:  # noqa
    """ Тут описано профилирование на Prometheus + Graphana. Особенность: полноценный мониторинг в вебе, но строится достаточно сложно. Ниже структура проекта. """  # noqa
    @staticmethod
    def information():
        info = """
        Prometheus - инструмент мониторинга, установка для flask: pip install prometheus-flask-exporter.
        Graphana - инструмент визуализации мониторинга, т.е. типа веб-интерфейс.

        Структура: главная папка в которой лежит все остальное:
            1) app/ папка, внутри которой: приложение routes.py(или иначе), Dockerfile, requirements.txt(flask, prometheus_flask_exporter)
            2) prometheus.yml - конфиг для prometheus
            3) docker-compose.yml - для запуска этого всего вместе

        команда: docker-compose up запускает все это дело
        Информацию от prometheus искать по адресу: /metrics, стандартный порт: 9090, указывается в конфигах. В этом случае стоит 5000
        Так же в config у prometheus есть эндпоинты before и after request 

        localhost:3000/login - интерфейс graphana | admin / admin - default данные для входа, там же можно настроить графики. 
        
        Настройки в Graphana - Data Sources: # noqa
        Name: random - будет использоваться при взятии данных в графике , Type: Prometheus
        HTTP: url: http://prometheus:9090 # prometheus из конфига и порт из конфига (его дефолт. веб-интерфейс). """  # noqa

        dockerfile = """ 
            FROM python:3-alpine
            ADD requirements.txt /tmp/requirements.txt
            RUN pip install -r /tmp/requirements.txt
            ADD routes.py /var/server/app.py
            CMD python /var/server/app.py
        """  # Просто запускалка приложения для интеграции в docker-compose # noqa

        prometheus_yml = """ file prometheus.yml, конфиг файл, используется в файле docker-compose.yml для настройки
            global: # Глобальные настройки конфига
              scrape_interval:     3s # Интервал обновления всех метрик

              external_labels: # Объект мониторинга
                monitor: 'routes.py' # Произвольное название, но сделано от файла приложения до build в контейнере


            scrape_configs: # Конфиг конкретного приложения
              - job_name: 'prometheus' # Имя конфигурируемого приложения: берется из docker-compose.yml (prometheus:...)
                scrape_interval: 5s # Интервал для сбора метрик
                static_configs: # Адрес для сбора конфига (localhost - дефолт, порт 9090 - дефолт, так же указан в docker-compose.yml) # noqa
                  - targets: ['localhost:9090']

              - job_name: 'flask'
                scrape_interval: 5s
                static_configs:
                    - targets: [ "app:5000" ]

                dns_sd_configs:
                  - names: ['app.py'] # имя сканируемого файла с приложением
                    port: 5000 # порт для доступа к сканируемому приложению
                    type: A
                    refresh_interval: 5s # Интервал обновления значений мониторинга
        """  # В нем параметры Prometheus # noqa

        docker_compose = """ file docker-compose.yml, описание есть в разделе docker
            version: '3.9'
            services:

              app:
                build:
                  context: app
                stop_signal: SIGKILL
                ports:
                  - 5000:5000

              generator:
                build:
                  context: generator
                stop_signal: SIGKILL

              prometheus:
                image: prom/prometheus:v2.46.0
                volumes:
                  - ./prometheus/config.yml:/etc/prometheus/config.yml
                ports:
                  - 9090:9090
                environment:
                  TZ: "Europe/Moscow"

              grafana:
                image: grafana/grafana:5.2.2
                ports:
                  - 3000:3000
        """  # В нем уже и описывается подключение Graphana # noqa
        return info, dockerfile, prometheus_yml, docker_compose

    @staticmethod
    def routes_py():  # Prometheus только.  # noqa
        """ Тут минимальная структура файла routes.py, тут настраивается только Prometheus без Graphana. """  # noqa
        from prometheus_flask_exporter import PrometheusMetrics  # noqa
        from flask import Flask  # noqa

        app = Flask(__name__)
        metrics = PrometheusMetrics(app)

        @app.route()
        @metrics.counter('ONE_200', 'one 200 status code', labels={'status': lambda resp: resp.status_code})
        def one():
            """ Декоратор counter собирает количество различных статус кодов, которые возвращает эндпоинт"""  # noqa
            return 'OK', 200

        if __name__ == '__main__':
            app.run('0.0.0.0', 5000, threaded=True)


class SentryProfiler:
    """ Еще один инструмент настройки профилирования приложения. Особенность: отдельный сервис со своим сайтом и настройками, но частично платный.
            Для flask: pip install --upgrade 'sentry-sdk[flask]'. Стоит идти по документации, она динамическая в зависимости от интеграций и проекта. """
    from sentry_sdk.integrations.flask import FlaskIntegration  # noqa
    from flask import Flask  # noqa
    import sentry_sdk  # noqa

    sentry_sdk.init(  # dsn - прямо на сайте генерируется, оттуда и копируется # noqa
        dsn="https://bd5dd6706d02391dee51f86068ef5156@o4506766790230016.ingest.sentry.io/4506766795145216",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    app = Flask(__name__)

    @app.route("/")
    def hello_world():  # noqa
        1 / 0  # raises an error # noqa
        return "<p>Hello, World!</p>"
