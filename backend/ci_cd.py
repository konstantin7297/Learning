class Test:
    """ Тут описана информация по составлению тестов приоритетно на 'pytest'. """
    def info(self):  # noqa
        info = """ 
        Установка: 'pip install pytest'. Он поддерживает плагины: 'https://docs.pytest.org/en/7.0.x/reference/plugin_list.html#plugin-list'.
        Файлы с тестами должны называться в формате 'test_bla.py'.
        Значения тестов: '.' - Пройден, 'F' - False, 'E' - Exception.
        """  # Общая информация. # noqa

        commands = {
            "pytest": "Запустит все тесты в директории.",
            "pytest test_function.py": "Запустит файл с тестами 'test_function.py'.",
            "pytest -v": "Запустит тесты и выведет более подробный результат тестирования.",
            "pytest -k math": "Запустит тесты, в названии которых есть 'math'.",
            "pytest -m math": "Запустит тесты, на которых стоит декоратор 'math'.",
            "pytest --markers": "Список доступных маркеров, как встроенных, так и кастомных.",
        }  # Консольные команды для работы с pytest. # noqa

        scope = {
            "function": "Область действия по умолчанию, fixture уничтожается в конце теста.",
            "class": "Приспособление уничтожается во время демонтажа последнего теста в классе.",
            "module": "Приспособление уничтожается во время демонтажа последнего теста в модуле.",
            "package": "Приспособление уничтожается во время разборки последнего теста в упаковке.",
            "session": "Приспособление уничтожается в конце сеанса тестирования.",
        },  # Параметры scope. Указывает, когда нужно закрывать fixture. # noqa

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
        }  # Типы тестов. # noqa
        return info, commands, scope, tdd, bdd, test_types

    @staticmethod  # Тут настраивается конфигурация для самого pytest. Например: создание маркеров, игнорирование конкретных ошибок...
    def pytest_ini():  # Файл: 'pytest.ini'. Необязательный файл. # noqa
        """ В нем описываются маркеры. Они делят тесты на секции и позволяют запускать часть конкретных тестов. Необязательный файл. """
        pattern = """
        [pytest]  
        markers =  # При запуске тестов можно указать -m math, тогда будут запущены только отмеченные маркером тесты.
            math: математическая функция
            
        filterwarnings =  # Тут пример, как можно проигнорировать какую-то ошибку.
            error
            ignore::marshmallow.warnings.RemovedInMarshmallow4Warning
        """  # noqa
        return pattern

    @staticmethod  # Тут настраиваются глобальные переменные для остальных тестов. Например: создание сессии базы данных или приложение.
    def conftest_py():  # Файл: 'conftest.py'. # noqa
        """ В нем описываются fixture, они нужны для создания данных под тесты. Например: 'session'. """
        @pytest.fixture  # Пример fixture, которая отдает клиент для дальнейшей работы. По сути пустышка для примера. # noqa
        def get_client():
            return MailAdminClient()  # noqa

        @pytest.fixture(scope="module")  # Пример fixture, которая может подать аргумент в функцию: '@pytest.mark.arg(42)'. # noqa
        def arg_to_func(request):  # arg_to_func будет == 42. # noqa
            if marker := request.node.get_closest_marker("arg"):
                return marker.args[0]  # Вернет поданный аргумент или неявно None.

        @pytest.fixture  # finalizer - создает действие для fixture, которые будет выполнено в конце теста. Например: удаление пользователя после теста. # noqa
        def get_user(get_client, request):  # Запрашивает клиент у другой fixture.
            user = get_client.create_user()

            def delete_user():  # Функция для дальнейшего выполнения.
                get_client.delete_user(user)

            request.addfinalizer(delete_user)  # Говорим fixture, что делать после теста.
            return user  # noqa

        @pytest.fixture  # Аналог finalizer - позволяет создать действия ДО и ПОСЛЕ запроса к fixture. Например: 'создание' - 'использование' - 'удаление'. # noqa
        def get_user_2(get_client):
            user = get_client.create_user()
            yield user  # noqa
            get_client.delete_user(user)  # noqa

    @staticmethod  # Тут пишутся сами тесты.
    def test_func_py():  # Файл: 'test_func.py'. # noqa
        """ В нем лежат сами тесты. Важно, что файл и функции тестов должны начинаться на 'test_'. """
        from unittest.mock import patch, Mock, MagicMock  # Mock - имитирует поведение каких либо функций, позволяя еще собирать статистику.  # noqa

        @patch('requests.get')  # Позволяет заменить 'requests.get(...)' на fake функцию для тестов и определить фиксированные данные ее возвращения.  # noqa
        def test_mock(my_patch):  # Принимает объект 'my_patch', который содержит в себе созданный в '@patch(...)' fake 'requests.get'.  # noqa
            """ Mock - это функции, которые имитируют поведение других функций, тем самым позволяют избавиться от зависимостей в тестах от не нужных вещей.
            @patch(...) - Декоратор или контекстный менеджер, который позволяет заменить объект или функцию на мок-объект (mock object) во время выполнения теста.
            Mock(...) - Позволяет создавать объекты, которые имитируют поведение реальных объектов, но дают вам полный контроль над их поведением.
            MagicMock(...) - Подкласс 'Mock', добавляет магические методы (__getattr__, ...), что позволяет ему более гибко имитировать поведение реальных объектов.
            """  # Моки так же позволяют получать некоторую статистику, например кол-во вызовов функции и т.д. # noqa
            mock = Mock()  # Создание fake класса-пустышки. Тут же можно подать некоторые атрибуты.  # noqa
            magic_mock = MagicMock()  # Создание fake класса с магическими методами. Тут же можно подать некоторые атрибуты.  # noqa

            my_patch.return_value.json.return_value = {'data': 'mocked'}  # Указывает, что будет возвращать 'requests.get(...).json()' при вызове.  # noqa
            mock.my_method.return_value = 'return'  # Указывает, что будет возвращать 'mock.my_method(...)' при вызове.  # noqa
            magic_mock.__str__.return_value = 'true'  # Указывает, что будет возвращать 'magic_mock.__str__' при вызове.  # noqa

            assert requests.get(url).json() == {'data': 'mocked'}  # Пример успешного выполнения теста с fake 'patch' функцией.  # noqa
            assert mock.my_method() == 'return'  # Пример успешного выполнения теста с fake 'Mock' функцией.  # noqa
            assert magic_mock.__str__ == 'true'  # Пример успешного выполнения теста с fake 'MagicMock' функцией.  # noqa

        @patch('file.func_name')  # patch - Заменяет реальную функцию на fake для теста в виде MagicMock.  # noqa
        def test_mock(func_name):  # Функции тестов всегда начинаются на 'test_'. test_uppercase(smtp_connection) - берет 'smtp_connection' fixture.  # noqa
            func_name.return_value = 'result'  # Указывает, что будет возвращать fake функция в тесте при обращении к ней. # noqa
            assert func_name() == 'result'  # Теперь при запуске теста, если он будет использовать функцию из другого файла, то она будет заменяться на fake.  # noqa

        @pytest.mark.math  # mark - отмечает тест указанным тегом, позволяя потом вызывать только тесты конкретных тегов.  # noqa
        @pytest.mark.arg(42)  # Пример передачи аргументов в функцию через marker. # noqa
        def test_fixt(arg_to_func):  # Например: @pytest.mark.arg(42) - подача данных в маркер.
            assert arg_to_func == 42

        @pytest.mark.parametrize("degree, result", [(25, 5), (36, 6)])  # noqa
        def test_math_sqrt(degree, result):  # parametrize - по очереди передает кучу значений (многократный тест с разными данными).
            assert math.sqrt(degree) == result  # noqa

    @staticmethod  # Пример составления сразу нескольких зависимых друг от друга тестов.
    def series_pattern():  # noqa
        def conftest_py():  # noqa
            @pytest.fixture(scope="class")  # Создает пользователя в клиенте.  # noqa
            def user(admin_client):
                _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")  # noqa
                admin_client.create_user(_user)
                yield _user
                admin_client.delete_user(_user)

            @pytest.fixture(scope="class")  # Запускает псевдо-браузер # noqa
            def driver():
                _driver = Chrome()  # noqa
                yield _driver
                _driver.quit()

            @pytest.fixture(scope="class")  # Возвращает страницу HTML  # noqa
            def landing_page(driver, login):  # noqa
                return LandingPage(driver)  # noqa

        def test_func_py():  # noqa
            class TestLandingPageSuccess:  # noqa
                @pytest.fixture(scope="class", autouse=True)  # Авторизуется на странице.  # noqa
                def login(self, driver, base_url, user):
                    driver.get(urljoin(base_url, "/login"))  # noqa
                    page = LoginPage(driver)  # noqa
                    page.login(user)  # noqa

                def test_name_in_header(self, landing_page, user):  # Проверяет приветственное сообщение
                    assert landing_page.header == f"Welcome, {user.name}!"

                def test_sign_out_button(self, landing_page):  # Проверяет наличие кнопки на экране
                    assert landing_page.sign_out_button.is_displayed()

                def test_profile_link(self, landing_page, user):  # Проверяет ссылку на пользователя
                    profile_href = urljoin(base_url, f"/profile?id={user.profile_id}")  # noqa
                    assert landing_page.profile_link.get_attribute("href") == profile_href

    @staticmethod  # Пример составления интеграционных тестов.
    def integration_pattern():  # noqa
        def conftest_py():  # noqa
            @pytest.fixture  # Создает приложение + базу данных для тестов.  # noqa
            def app():
                _app = app  # Берем копию настроенного приложения вместе с эндпоинтами и т.д. # 'from routes.py import app'. # noqa
                _app.config["TESTING"] = True  # Можно донастроить копию приложения под тесты. # noqa
                _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"  # Тестовая БД будет прям в памяти ПК. # noqa
                _db.init_app(_app)  # Берем копию БД и подключаем БД + Приложение. # 'from models.py import db as _db'. # noqa

                with _app.app_context():
                    _db.create_all()  # Создаем таблицы БД для тестов.  # noqa
                    _db.session.add(User(id=1, name="name", surname="surname", email='mail'))  # Добавляем запись в БД.  # noqa
                    _db.session.commit()  # noqa
                    yield _app  # Возвращаем приложение с запущенной БД с 1 записью.
                    _db.session.close()  # После тестов закрываем все и удаляем.  # noqa
                    _db.drop_all()  # noqa

            @pytest.fixture  # Создает тестовый клиент с настроенным для тестов приложением из fixture 'app'.  # noqa
            def client(app):
                client = app.test_client()
                yield client

            @pytest.fixture  # Создает тестовую БД с настроенными записями для тестов БД из fixture 'app'.  # noqa
            def db(app):
                with app.app_context():
                    yield _db  # noqa

        def test_func_py():  # noqa
            def test_get_user(client) -> None:  # Тест на получение пользователя из БД.   # noqa
                response = client.get("/users/1")  # Запрашиваем user_id == 1 из БД.
                assert response.status_code == 200
                assert response.json == {"id": 1}  # Полученный пользователь.  # noqa

    @staticmethod
    def unittest():  # noqa
        """ Полностью готовая заготовка для тест кейса: просто скопировать все в новый файл. Альтернативный вариант тестирования """  # noqa
        import json
        import unittest
        from unittest.mock import Mock, MagicMock, patch  # Mock - позволяют заменить реальные компоненты системы на фиктивные. # noqa
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


class CI_CD:  # noqa
    """ Тут расписано все, что касается CI/CD реализации в проекте. """
    @staticmethod
    def information():
        ci = """ CI - процесс интеграции кода, т.е. готовый код грузится и отправляется на merge в главный репозиторий, в
        котором этот код проверяется на наличие всевозможных ошибок, косяков, оформления и т.д., что бы не было косяков
        с дальнейшей работой над отправленным кодом. CI можно настроить в репозитории и заключается он в запуске
        проверок, в которые входят: тесты, линтеры и т.д.

        Gitlab пример:
            1) Требуется зайти на сайт в репозиторий в раздел: 'настройки' -> 'CI/CD'.
            2) Там создать сборочную линию, после чего в корне проекта появится файл: '.gitlab-ci.yml'.
            3) Настроить файл '.gitlab-ci.yml'. Там устанавливается как CI, так и CD часть. """  # noqa

        cd = """ CD - процесс, который после прохождения CI и успешной интеграции в код - этот обновленный код начинает автоматически разворачиваться
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
        return ci, cd

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
