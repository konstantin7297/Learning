class CI:
    """ Тут расписано все, что касается CI реализации в проекте. """
    @staticmethod
    def information():
        """ CI - процесс интеграции кода, т.е. готовый код грузится и отправляется на merge в главный репозиторий, в
        котором этот код проверяется на наличие всевозможных ошибок, косяков, оформления и т.д., что бы не было косяков
        с дальнейшей работой над отправленным кодом. CI можно настроить в репозитории и заключается он в запуске
        проверок, в которые входят: тесты, линтеры и т.д.

        Gitlab пример:
            1) Требуется зайти на сайт в репозиторий в раздел: 'настройки' -> 'CI/CD'.
            2) Там создать сборочную линию, после чего в корне проекта появится файл: '.gitlab-ci.yml'.
            3) Настроить файл '.gitlab-ci.yml'. Там устанавливается как CI, так и CD часть. """  # noqa

    @staticmethod
    def test_info():
        """ Методы написания тестов и типы тестов. """
        tdd = """ TDD метод тестирования работает по схеме: Red -> Green -> Refactor -> Red -> Green -> Refactor...
        Принцип работы:
            1) Создается заготовка провального теста (Red).
            2) По нему описывается приложение до уровня успешного прохождения теста (Green).
            3) Еще больше описывается приложение (Refactor).
            4) Повторяются пункты 1, 2, 3. 
        """  # Принцип: пишется провальный тест -> по нему описывается приложение до прохождения теста -> по кругу... # noqa

        bdd = """ BDD метод тестирования работает по схеме сценария с ключевыми словами на английском языке. Такого сценария должны придерживаться все участники проекта.
        Запуск: 'pytest --generate-missing --feature login.feature', где файл сценария features/login.feature (from pytest_dbb import Given...).
        Принцип работы:
            1) Создается файл со сценарием. Например 'features/login.feature' (Пример на русском, но нужно на английском):
                Scenario: Вход в приложение
                    Given Пользователь заходит на страницу авторизации
                    When Пользователь вводит свой логин и пароль
                    And кликает на кнопку войти
                    Then Пользователь прошел авторизацию и видит стартовую страницу
            2) Создается файл с тестами, который будет идти по этапам сценария. Например:
                @scenario("../features/login.feature", "Вход в приложение")
                def test_enter_in_app():
                    pass

                Далее второй этап: Given Пользователь заходит на страницу авторизации:
                @given("Пользователь заходит на страницу авторизации")
                def user_is_on_login_page():
                    pass
        """  # Принцип: создается сценарий ожидаемого поведения -> по нему описывается приложение до прохождения теста. # noqa

        test_types = {
            "unit": "Тестирование отдельных модулей. Например функции или методы классов по отдельности. 1 уровень тестирования.",  # noqa
            "integration": "Тестирование взаимодействия модулей. Например приложение вместе с базой данной одновременно. 2 уровень тестирования.",  # noqa
            "system": "Системное тестирование. Тестируется работоспособность всей системы. 3 уровень тестирования.",  # noqa
            "E2E": "Пользовательское тестирование. Тестируется работоспособность всей системы, но уже пользователями. 4 уровень тестирования.",  # noqa
        }

        return tdd, bdd, test_types

    @staticmethod
    def linter_info():
        """ Информация по поводу линтеров (Статические анализаторы кода). Это проверка кода на соблюдение различных правил. """

        black = """ Установка: 'pip install black'.
        Запуск: 'black file.py' - простой запуск, который исправит код под свои ГОСТы.
        Запуск: 'black --check --diff file.py' - запуск с флагами, где
            --check - выполнит проверку без фактических исправлений файлов.
            --diff - выведет разницу, которую захочет увидеть в отношении нынешней версии (покажет, что хочет исправить). """  # noqa

        isort = """ Установка: 'pip install isort'.
        Запуск: 'isort --check-only --diff --profile black file.py', выполнит работу в зависимости от флагов, где
            --check-only - выполнит проверку без фактических исправлений файлов.
            --diff - выведет разницу, которую захочет увидеть в отношении нынешней версии (покажет, что хочет исправить).
            --profile - обеспечивает совместимость с другим линтером. Невилирует случай, когда 2 линтера меняют по разному одно место в коде. """  # noqa

        flake8 = """ Установка: 'pip install flake8==4.0.1 flake8-bugbear==22.1.11 flake8-pie==0.15.0', Так же устанавливает некоторые плагины для расширения проверки.
        Запуск: 'flake8 --max-line-length 99 homework/', проверит все файлы в 'homework/', с указанными флагами, где 
            --max-line-length - максимальная допустимая длина строки. """  # noqa

        mypy = """ Установка: 'pip install mypy types-flask'. 'types-flask' - плагин для поддержки Flask. Так можно написать свои плагины для более уникальной проверки.
        Запуск: 'mypy file.py', выполнит проверку с указанными параметрами. """  # noqa

        return black, isort, flake8, mypy

    @staticmethod
    def unittest():  # noqa
        """ Полностью готовая заготовка для тест кейса: просто скопировать все в новый файл. Альтернативный вариант тестирования """  # noqa
        import json
        import unittest
        from typing import Any, Dict
        from file import app  # Импорт приложения из файла с ним, соответственно оно и будет тестироваться # noqa

        class TestFile(unittest.TestCase):  # noqa
            """Тест кейс для тестирования корректности работы приложения"""
            @classmethod
            def setUpClass(cls) -> None:
                """Функция взаимодействия, запускающаяся перед началом тестов"""
                app.config['TESTING']: bool = True
                app.config['WTF_CSRF_ENABLED']: bool = False
                app.config['DEBUG']: bool = False
                cls.app: Any = app.test_client()
                cls.url: str = '/url'

            def setUp(self) -> None:
                """Функция взаимодействия, запускающаяся перед каждым тестом"""
                self.data: Dict = {
                    'first': 'first',
                    'second': 'second'
                }

            def test_true(self) -> None:
                """Тест на корректность работы"""
                self.data['first']: str = 'true_value'
                data: str = json.dumps(self.data)
                response: Any = self.app.post(self.url, data=data, headers={"content-Type": "application/json"})

                if response.status_code == 200:
                    result: Any = response.data.decode()
                else:
                    result: Any = None

                self.assertTrue(result)

            def test_false(self) -> None:
                """Тест на получение предусмотренного исключения"""
                self.data['second']: str = 'false_value'
                data: str = json.dumps(self.data)
                response: Any = self.app.post(self.url, data=data, headers={"content-Type": "application/json"})

                with self.assertRaises(AssertionError):
                    assert response.status_code != 200

        if __name__ == '__main__':
            unittest.main()

    gitlab_ci_yml = """ Описан пример файла '.gitlab-ci.yml', в котором строится CI часть.
    workflow:
        rules:
            - if: $CI_PIPELINE_SOURCE == "merge_request_event" # Запуск проверки при merge request
            - if: $CI_PIPELINE_SOURCE == "push" # Запуск проверки при загрузке в репозиторий

    image: python:3.10 # docker-image для установки всего остального

    stages: # Стадии проверки, сперва запускается стадия 'tests', потом 'linters'...
        - tests
        - linters
        - deploy

    before_script: # Перед началом проверки в image будут установлены все зависимости
        - pip install -r requirements.txt

    unittest: # В стадии 'tests' будет запущен скрипт(запуск тестов из папки): pytest tests/
        stage: tests
        script:
            - pytest tests

    mypy: # На стадии 'linters' будет запущен скрипт проверки линтером всех файлов в папке(в общем просто команда для консоли): mypy homework/
        stage: linters
        script:
            - mypy homework/

    black:
        stage: linters
        script:
            - black --diff --check homework/

    isort:
        stage: linters
        script:
            - isort --profile black --check-only homework/

    flake8:
        stage: linters
        script:
            - flake8 --max-line-length 99 homework/

    deploy_to_prod: # Запускает автоматический деплой на стадии 'deploy', после прохождения тестов и линтеров.
        stage: deploy
        script: # Скрипт сперва устанавливает библиотеку для авто-деплоя 'fabric', после чего запускает скрипт из файла fabfile.py -> deploy функцию.
            - pip install fabric
            - fab deploy
        only: # Запускает деплой только при изменениях master ветки репозитория.
            - master
    """  # Описан пример файла '.gitlab-ci.yml', в котором строится CI часть. # noqa

    pytest = {  # Тут не показаны используемые импорты для сохранения читаемости.
        "info": """
                Установка: 'pip install pytest==7.0.1'. Файлы с тестами должны быть формата: 'test_blabla.py'. Если при запуске не указывать название файла, запустятся все файлы с тестами.
                Значения тестов:
                    1) '.' - тест пройден.
                    2) 'F' - тест не пройден.
                    3) 'E' - непредвиденное исключение.
                Плагины для pytest: https://docs.pytest.org/en/7.0.x/reference/plugin_list.html#plugin-list. 
            """,  # Основная информация о библиотеке 'pytest'. # noqa
        "commands": {
            "pytest": "Запустит все тесты в директории",
            "pytest test_function.py": "Запустит файл с тестами test_function.py",
            "pytest -v": "Запустит тесты и выведет более подробный результат тестирования",
            "pytest -k math": "Запустит тесты, в названии которых есть 'math'",
            "pytest -m math": "Запустит тесты, на которых стоит декоратор 'math'",
            "pytest --markers": "Список доступных маркеров, как встроенных, так и кастомных",
        },  # Консольные команды для работы с pytest. # noqa
        "parameters": {
            "function": "Область действия по умолчанию, fixture уничтожается в конце теста.",
            "class": "Приспособление уничтожается во время демонтажа последнего теста в классе.",
            "module": "Приспособление уничтожается во время демонтажа последнего теста в модуле.",
            "package": "Приспособление уничтожается во время разборки последнего теста в упаковке.",
            "session": "Приспособление уничтожается в конце сеанса тестирования.",
        },  # Параметры scope. # noqa
        "pytest.ini": "Тут настраивается конфигурация для самого pytest. Например: создание маркеров, игнорирование конкретных ошибок...",  # noqa
        "conftest.py": "Тут настраиваются глобальные переменные для остальных тестов. Например: создание сесии базы данных или приложение.",  # noqa
        "test_function.py": "Тут пишутся сами тесты.",  # noqa
        "--------------------------- Примеры -----------------------------": "--------------------------- Примеры -----------------------------",
        "marker + fixture": """  # Тут описаны мелкие примеры основных штук.
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa

                        [pytest]  # При запуске тестов можно указать -m math, тогда будут запущены только отмеченные маркером тесты.
                        markers=
                            math:математическая функция

                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa

                        @pytest.fixture(scope="module")  # Пример создания fixture с конкретным режимом работы. # noqa
                        def smtp_connection():  # scope можно не указывать.
                            return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)  # Создается mail session.

                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        @pytest.mark.math  # Самый простой тест, можно даже '@pytest.mark.math' убрать.
                        def test_uppercase():  # Функции тестов всегда начинаются на 'test_'. test_uppercase(smtp_connection) - берет 'smtp_connection' fixture.
                            assert "skillbox".upper() == "SKILLBOX"
            """,  # Тут описаны marker, fixture для примера, как с ними вообще работать. Основа и синтаксис. # noqa
        "marker_values": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa

                        @pytest.fixture  # Если в тесте подать '@pytest.mark.fixt_data(42)'
                        def fixt(request):  # То fixt будет == 42.
                            marker = request.node.get_closest_marker("fixt_data")
                            if marker is None:
                                data = None
                            else:
                                data = marker.args[0]
                            return data

                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        @pytest.mark.fixt_data(42)
                        def test_fixt(fixt):
                            assert fixt == 42
            """,  # Пример передачи аргументов через marker. Например: @pytest.mark.fixt_data(42) - подача данных в маркер.  # noqa
        "parametrize": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa
                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        @pytest.mark.parametrize("degree, result", [(25, 5), (36, 6)])
                        def test_math_sqrt(degree, result):  # parametrize - по очереди передает кучу значений (многократный тест с разными данными).
                            assert math.sqrt(degree) == result
            """,  # Тест сразу списка данных одного формата. Например: [1, 2, 3] - запуск теста для каждого элемента в списке.  # noqa
        "yield": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa

                        @pytest.fixture
                        def mail_admin():
                            return MailAdminClient()

                        @pytest.fixture
                        def get_one(mail_admin):
                            user = mail_admin.create_user()
                            yield user
                            mail_admin.delete_user(user)

                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        def test_check(get_one):
                            assert get_one is True
            """,  # Для каждого теста будут создаваться новые данные. Например: при каждом тесте значение будет создаваться заного. # noqa
        "finalizer": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa

                        @pytest.fixture
                        def mail_admin():
                            return MailAdminClient()

                        @pytest.fixture
                        def get_one(mail_admin, request):
                            user = mail_admin.create_user()

                            def delete_user():
                                mail_admin.delete_user(user)

                            request.addfinalizer(delete_user)
                            return user

                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        def test_check(get_one):
                            assert get_one is True

            """,  # Он создает действие для fixture, которое будет выполнено в конце теста. Например: удаление пользователя после теста. # noqa
        "many_assert": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa

                        @pytest.fixture(scope="class")
                        def admin_client(base_url, admin_credentials):  # Создает клиент
                            return AdminApiClient(base_url, **admin_credentials)

                        @pytest.fixture(scope="class")  # Создает пользователя в клиенте
                        def user(admin_client):
                            _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
                            admin_client.create_user(_user)
                            yield _user
                            admin_client.delete_user(_user)

                        @pytest.fixture(scope="class")  # Запускает псевдо-браузер # noqa
                        def driver():
                            _driver = Chrome()
                            yield _driver
                            _driver.quit()

                        @pytest.fixture(scope="class")  # Возвращает страницу HTML
                        def landing_page(driver, login):  # noqa
                            return LandingPage(driver)

                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        class TestLandingPageSuccess:
                            @pytest.fixture(scope="class", autouse=True)  # Авторизуется на странице
                            def login(self, driver, base_url, user):
                                driver.get(urljoin(base_url, "/login"))
                                page = LoginPage(driver)
                                page.login(user)

                            def test_name_in_header(self, landing_page, user):  # Проверяет приветственное сообщение
                                assert landing_page.header == f"Welcome, {user.name}!"

                            def test_sign_out_button(self, landing_page):  # Проверяет наличие кнопки на экране
                                assert landing_page.sign_out_button.is_displayed()

                            def test_profile_link(self, landing_page, user):  # Проверяет ссылку на пользователя
                                profile_href = urljoin(base_url, f"/profile?id={user.profile_id}")
                                assert landing_page.profile_link.get_attribute("href") == profile_href
            """,  # Тут пример запуска сразу нескольких операторов assert. Например: цепочка зависимых друг от друга тестов. # noqa
        "ignore_error": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                        [pytest]
                        filterwarnings =
                            error
                            ignore::marshmallow.warnings.RemovedInMarshmallow4Warning

                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa
                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa
            """,  # Тут пример, как можно проигнорировать какую-то ошибку. # noqa
        "pattern_integration": """
                # Файл: pytest.ini  # В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. # noqa
                # Файл: conftest.py  # В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. # noqa

                        @pytest.fixture  # Создает приложение + базу данных для тестов.
                        def app():  
                            _app = app  # Берем копию настроенного приложения вместе с эндпоинтами и т.д. # 'from routes.py import app'. # noqa
                            _app.config["TESTING"] = True  # Можно донастроить копию приложения под тесты. # noqa
                            _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"  # Тестовая БД будет прям в памяти ПК. # noqa
                            _db.init_app(_app)  # Берем копию БД и подключаем БД + Приложение. # 'from models.py import db as _db'. # noqa

                            with _app.app_context():
                                _db.create_all()  # Создаем таблицы БД для тестов.
                                _db.session.add(User(id=1, name="name", surname="surname", email='mail'))  # Добавляем запись в БД.
                                _db.session.commit()
                                yield _app  # Возвращаем приложение с запущенной БД с 1 записью.
                                _db.session.close()  # После тестов закрываем все и удаляем.
                                _db.drop_all()

                        @pytest.fixture  # Создает тестовый клиент с настроенным для тестов приложением из fixture 'app'.
                        def client(app):
                            client = app.test_client()
                            yield client

                        @pytest.fixture  # Создает тестовую БД с настроенными записями для тестов БД из fixture 'app'.
                        def db(app):
                            with app.app_context():
                                yield _db

                # Файл: test_function.py  # В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. # noqa

                        def test_get_user(client) -> None:  # Тест на получение пользователя из БД. 
                            response = client.get("/users/1")  # Запрашиваем user_id == 1 из БД.
                            assert response.status_code == 200
                            assert response.json == {"id": 1, ...}  # Полученный пользователь.
            """,  # Пример интеграционного теста. Например: приложение Flask + База данных вместе. # noqa
    }


class CD:
    """ Тут расписано все, что касается CD реализации в проекте. """
    @staticmethod
    def information():
        """ CD - процесс, который после прохождения CI и успешной интеграции в код - этот обновленный код начинает автоматически разворачиваться
        там, где нужно (будь это сервер или что-то еще).

        Установка CD:
            1) В корне проекта создается файл: 'fabfile.py', в котором описываются инструкции CD. Запустить можно командой 'fab deploy', где deploy - название функции.
                Сама функция получает обязательный аргумент - контекст, который содержит словарь с необходимыми служебными переменными.

            2) На удаленном сервере настраивается подключение к репозиторию через SSH ключ:
                а) Создать новый ключ в папке .ssh пользователя (/home/ec2-user/.ssh/): 'ssh-keygen -t rsa'.
                б) .pub ключ нужно сохранить в настройках репозитория на сайте.
                в) Проверить можно ли спулить репозиторий на сервере.

            3) Зайти в 'репозиторий' -> 'CI/CD' -> 'Variables'. Там нужно добавить все переменные (так же указать их тип), которые нужно спрятать от публичного
                доступа (Типа .env информацию). Обращаться к ним можно из файла 'fabfile.py' аналогично импорту из '.env' файла через: 'os.environ["KEY"]'.
                Переменные из этого шаблона для примера:
                    а) EC2_HOST - значение ip адрес сервера, где будет работать приложение.
                    б) EC2_USER_NAME - ec2-user, имя пользователя авторизации с сервера.
                    в) EC2_PRIVATE_KEY - ./test-rsa - путь до приватного ключа на сервере приложения. Пример: /home/ec2-user/.ssh/name_key.pub - публичный ключ.

            4) Далее добавить этот настроенный CD в конфигурацию к CI в файл: '.gitlab-ci.yml' с предпочтительным вариантом запуска (Например чтобы он
                запускал деплой на мерже в мастер). """  # noqa

    fabfile_py = """ Описан пример файла 'fabfile.py', в котором строится CD часть.
    import os
    from fabric import task, Connection

    @task
    def deploy(ctx):
       with Connection(
               os.environ["EC2_HOST"],  # Хост сервера, куда нужно подключиться (где будет работать приложение)
               user=os.environ["EC2_USER_NAME"],  # Имя пользоваться, которым авторизуемся на сервере, от его лица выполняются действия, а не от root'а
               connect_kwargs={"key_filename": os.environ["EC2_PRIVATE_KEY"]}  # Приватный ssh ключ на сервере приложения (точнее путь до него)
       ) as c:
          with c.cd("/home/ec2-user/automated-deployment"):  # Заходим в папку с кодом приложения (Собственно путь до директории приложения)
             c.run("docker-compose down")  # Останавливает приложение, если оно запущено
             c.run("git pull origin master --rebase")  # Обновить код приложения (запулить изменения проекта)
             c.run("docker-compose up --build -d")  # Запустим обновленное приложение, пересобрав докеры
    """  # Описан пример файла 'fabfile.py', в котором строится CD часть. # noqa
