class Docker:
    """ Класс описывает работу с Docker. """
    @staticmethod
    def information():
        """ Тут описаны некоторые нюансы и интересные моменты при работе с Docker. Рестарт: sudo systemctl restart docker. """
        ban_fix = """
        Установка прокси:
            sudo mkdir -p /etc/systemd/system/docker.service.d
            sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf  # Далее пишем прокси:
                [Service]
                Environment="HTTP_PROXY=http://proxy-example.com:3128"
                Environment="HTTPS_PROXY=http://proxy-example.com:3128"
            sudo systemctl daemon-reload
            sudo systemctl restart docker
    
        Конфиг: ~/.docker/daemon.json  # Настройки применяются при сборке и в запущенных контейнерах.
        Конфиг: ~/.docker/config.json  # Настройки применяются к основной операционной системе.
            Добавление авторизации в него:
                {
                    "auths": {
                        "mirror-example.com": {
                            "auth": "dXNlcjp1c2Vy"
                        }
                    }
                }
    
            Добавление зеркал:
                {
                    "features": {
                        "containerd-snapshotter": true
                        },
                    "registry-mirrors": [
                        "https://dockerhub.timeweb.cloud/",
                        "https://mirror.gcr.io",
                        "https://daocloud.io",
                        "https://c.163.com/",
                        "https://registry.docker-cn.com"
                    ]
                } """  # noqa

        docker_ignore = """ Файл: '.dockerignore'. В нем хранятся файлы и папки, которые докер должен игнорировать:
            .idea
            .git
            Dockerfile
        """  # noqa

        makefile = """ Файл: 'Makefile'. Можно забиндить определенные команды консоли для удобного вызова, pip install make, запуск: 'make run': 
        run:
            docker run -d -p 80:4200 --env-file ./.env --rm --name test_cont test_cont:my_tags
        """  # noqa

        return ban_fix, docker_ignore, makefile

    @staticmethod
    def dockerfile():
        """ Тут расписано строение 'Dockerfile'. Сам файл обычно создается в корне проекта. """
        params = {
            "------------------------- Разновидности команд -------------------------": "------------------------- Разновидности команд -------------------------",
            "FROM python:3.10": "Задаёт базовый (родительский) образ. В данном случае Python 3.10 версии.",  # -slim-stretch - самая пустая версия с минимумом библиотек. # noqa
            "LABEL maintainer='jeffmshale@gmail.com'": "Описывает метаданные. Например — сведения о том, кто создал и поддерживает образ.",
            "ARG PASS='adw14km'": "Устанавливает переменные во время сборки контейнера. К ним нельзя обращаться после сборки контейнера.",
            "ENV ADMIN='jeff'": "Устанавливает постоянные переменные. После этого к ним можно обращаться через $ADMIN даже в этом же Dockerfile.",
            "RUN mkdir /app": "Позволяет выполнить команду внутри контейнера. В данном случае создает папку '/app'. 'WORKDIR /app может заменить эту команду, еще и войдет в папку.",
            "WORKDIR /app": "В этой директории будет запущен контейнер. Уже под этой командой консоль будет работать из этой папки.",
            "COPY base.txt prod.txt /app/": "Копирует файлы: основная ОС -> контейнер. В данном примере файлы base.txt и prod.txt - файлы с зависимостями.",
            "ADD https://site.ru/video.mp4 /app": "Копирует файлы и папки в контейнер. Может распаковывать локальные .tar-файлы и работать с ссылками.",
            "VOLUME /app/data": "Создает точку синхронизации Локальная ОС <-> Контейнер. docker run -v ubuntu_data/:/app/data - результат из /app/data будет в папке ubuntu_data",
            "EXPOSE 5000": "Открывает необходимый порт для подключения по нему к контейнеру.",
            "CMD ['python', 'app.py']": "Выполняет консольную команду только при запуске контейнера(внутри него). Если CMD/ENTRYPOINT несколько, работает только последний.",
            "ENTRYPOINT ['python', 'app.py']": "Выполняет консольную команду только при запуске контейнера(внутри него). Позволяет передавать доп. аргументы: 'docker run bla...'.",
            "------------------------- Шаблоны важных команд -------------------------": "------------------------- Шаблоны важных команд -------------------------",
            "ENV PYTHONUNBUFFERED=1": "Команда возвращает логи от контейнера в консоль.",  # noqa
            "RUN apt-get update && rm -rf /var/lib/apt/lists/*": "Обновляет apt-get установщик и удаляет его пакеты-установщики после установки.",
            "RUN python -m pip install --upgrade pip && python -m pip install --no-deps --no-cache-dir -r requirements.txt": """
                Команда сперва обновит установщик 'pip', затем начнет устанавливать зависимости из файла 'requirements.txt' с флагами:
                    --no-deps: устанавливает только зависимости из файла, не будет учитывать доп. зависимости самих зависимостей, которых нет в этом файле.
                    --no-cache-dir: устанавливает зависимости без кэширования пакетов. Это нужно для экономии места.
                """,  # Установка зависимостей через pip.
            "RUN pip install --upgrade pip 'poetry==1.4.2' && RUN poetry config virtualenvs.create false --local": """
                Команда сперва установит установщик 'poetry', затем обновит его конфиг (Выключает создание виртуального окружения, т.к. контейнер уже им является).
                Копируем зависимости для установки: COPY pyproject.toml poetry.lock ./
                Устанавливаем зависимости: RUN poetry install
                """,  # Установка аналога pip и работа с ним: 'poetry'.
        }

        python = """ Шаблон Dockerfile для приложения на Python.
            FROM python:3.12
            WORKDIR /app
            COPY requirements.txt .
            RUN python -m pip install --no-deps --no-cache-dir -r requirements.txt
            COPY src/ .
            CMD ["gunicorn", "--bind", "0.0.0.0:5000", "routes:app"]
        """  # Установка приложения на Python. # noqa

        django = """ Шаблон Dockerfile для приложения на Python - Django.
            FROM python:3.10
            ENV PYTHONUNBUFFERED=1
            WORKDIR /app
            RUN pip install --upgrade pip "poetry==1.4.2" && RUN poetry config virtualenvs.create false --local
            COPY pyproject.toml poetry.lock ./
            RUN poetry install
            COPY mysite .
            CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
        """  # Установка приложения на Python с помощью установщика 'poetry'. # noqa

        nginx = """  Шаблон Dockerfile для Nginx Web-сервера:
            FROM nginx
            RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
            COPY static/ /app/static/
            COPY nginx.conf /etc/nginx/nginx.conf 
        """  # 'static/' содержит такие файлы: 'index.html', 'style.css', 'script.js'. # noqa

        return params, python, django, nginx

    @staticmethod
    def console():
        """ Тут команды для работы с Docker. """
        commands = {
            "docker build -t test_app .": """Создает свой контейнер из указанной дирректории(.), в дирректории долнжы быть файлы requirements.txt, app.py, dockerfile. 
                    -f - указывает название Dockerfile, -t test_app - название контейнера, test_app:tag_name - через : можно указать тег для контейнера """,  # noqa
            "docker login": "авторизация в докер аккаунте",
            "docker tag test_app kas7297/test_app": "связывает локалку с удаленкой с помощью названия или делает копию с названием удаленного контейнера",  # noqa
            "docker push kas7297/test_app": "загружает с локалки на связанную удаленку",  # noqa
            "docker pull name/url": "скачивает докер по ссылке или имени",
            "docker images": "показывает список билдов",  # noqa
            "docker image prune": "удаляет все неиспользуемые image",
            "docker diff name_container": "показывает изменения указанного контейнера",
            "docker logs name_container": "показывает весь вывод в stdout и stdin за время работы контейнера",
            "docker volume ls": "показывает все временные файлы для параметра VOLUME",
            "docker ps": "выдает информацию об активном контейнере(название, ид и т.д.). -a может показать все контейнеры, -d позволяет запустить контейнер в фоновом режиме",
            "docker kill name": "закрывает запущенный контейнер",
            "docker stop name": "останавливает запущенный контейнер",
            "docker remove name": "удаляет остановленный контейнер",
            "docker rmi name": "удаляет image докера",
            "docker container prune": "удаляет все контейнеры",
            "docker start": "запускает докер контейнер",
            "docker run -p 5050:5000": """запускает докер image. 
                -i - интерактивный режим, который позволяет работать напрямую с stdin из консоли в контейнер, 
                -t - подключает к создаваемому терминалу внутри контейнера, 
                -e "ключ=значение" - позволяет передать значения в переменное окружение контейнера. Например -e PORT=3000 передает в dockerfile - ENV переменную,
                --env-file ./.env - передает файл с переменными,
                -p - передача портов, где 5050:5000 - это Локальный-порт:Контейнер-порт,
                --rm - удаляет контейнер после завершения работы,
                --name blabla - устанавливает имя для контейнера,
                -v logs:/app/data - создает переменную с временными файлами внутри докер контейнера, которая называется logs и лежит по пути /app/data """,
            "docker run -i -t debian bash": "запуск команды через докер, а именно запуск баш системы через докер",
            "docker run -p5050:5000 test_app python /app/app.py": "запускает приложение из контейнера",
            "sudo systemctl restart docker": "Рестарт системы Docker при изменении его конфигурации.",
            "docker exec -it <id_контейнера> uptime": "запускает команду внутри контейнера, где uptime - команда, sh - запустит консоль контейнера",  # noqa
            "docker cp container_name:/etc/info.md info.md": "Копирует из контейнера файл info.md на локальную машину",  # noqa
        }
        return commands


class DockerCompose:
    """ Класс описывает работу с docker-compose. Это addon для Docker, позволяющий объединять сеть контейнеров в 1 файле: 'docker-compose.yaml'. """
    @staticmethod
    def docker_compose_yaml():
        """ Тут расписано строение 'docker-compose.yaml' файла. Сам файл обычно создается в корне проекта. """
        params = """ Параметры для файла: 'docker-compose.yaml'.
        version: '3.9'  # Версия самого docker-compose, от нее зависят доступные команды и прочие мелочи.
        
        networks:  # Тут описываются локальные сети для docker-compose локальной сети. К примеру что-бы backend и frontend были связаны или нет.
            my_net:  # Название описываемой локальной сети. По нему можно подключать сервисы. Если не указано, то будет работать на все глобально.
                driver: bridge  # Драйвер для работы локальной docker-compose сети. Если он не установлен, вернет ошибку.
                
        services:  # Тут описываются все Docker-контейнеры, которые будут использоваться в этой сети.
            database:  # Docker с базой данных. Название любое.
                image: postgres  # image, который нужно использовать вместо билда нового контейнера.
                stop_signal: SIGKILL  # Комбинация CTRL + C выключит контейнер.
                restart: always  # В случае отката сервиса, он будет перезагружен. always - всегда.
                networks:  # Описаны, какие локальные сети будет использовать сервис.
                    - my_net  # Сервис будет подключен к сети back-end, и будет совместим с сервисами с такой же сетью.
                ports:  # Указывает порты, на которых будет работать сервис между докером и внешним миром.
                    - '5432:5432'  # Порт, на котором работает этот сервис: Основная ОС (:5432) <-> Докер ОС (:5432).
                volumes:  # Синхронизация переменных Основная ОС <-> Docker-контейнер.
                    - ./database/:/var/lib/postgresql/data  # В докере используется БД из основной ОС по пути 'database/'.
                environment:  # Указывает переменные окружения для сервиса.
                    - POSTGRES_USER=admin  # Логин для подключения к БД.
                    - POSTGRES_PASSWORD=admin  # Пароль для подключения к БД.
                    - POSTGRES_DB=db  # Название БД.
                healthcheck:  # Тут описывает алгоритм тестирования сервиса на работоспособность. Для Application: ['CMD-SHELL', 'curl -f http://localhost:8000/ || exit 1']
                    test: ['CMD-SHELL', 'pg_isready -d db -U admin']  # Команда, которая тестирует статус БД. ${DB_NAME} - взять из .env данные.
                    interval: 30s  # Интервал прохождения теста.
                    timeout: 60s  # Ожидание ответа теста.
                    retries: 5  # Попыток в случае провала.
                    start_period: 80s
                    
            server:  # Docker с серверной частью или же просто Backend. Название любое.
                build:  # Тут описывается то, что нужно билдить для запуска.
                    context: ./server  # Папка, где хранится Dockerfile.
                    dockerfile: Dockerfile  # Имя самого Dockerfile.
                container_name: my_container  # Имя, которое будет выдано создаваемому контейнеру.
                working_dir: '/application'  # Рабочая директория. В этой директории будет запущен контейнер.
                command: ['python', '-m', 'main.py']  # Команда, которую нужно выполнить внутри контейнера.
                env_file:  # При необходимости можно указать .env файл с переменными.
                    - '.env'  # Имя .env файла с переменными окружения.
                links:  # Указывает, какие сервисы нужно запустить перед этим сервисом.
                    - database  # База данных будет запущена раньше, чем server.
                depends_on:  # Описано, что нужно проверять на работоспособность.
                    database:  # Проверяем нашу базу данных.
                        condition: service_healthy  # Тип проверки: сервер запущен и работает.
                        
                logging:  # Секция описывает способ логирования приложения. Пример от Django, нужен только при наличии логирования.
                  driver: "json-file"  # Запись логов в json-файлы.
                  options:  # Набор параметров для логирования.
                    max-file: "10"  # Максимум 10 файлов с логами.
                    max-size: "200k" # Вес каждого файла с логами 200Кб.
        """  # Различные параметры с пояснениями. # noqa

        python = """ Шаблон для 'docker-compose.yaml' файла для работы с Python Django + PostgreSQL.
            version: '3.9'

            services:
              database:
                image: postgres:13.15
                container_name: database-1
                stop_signal: SIGKILL
                restart: always
                env_file:
                  - '.env'
                ports:
                  - '${PG_PORT}:5432'
                volumes:
                  - ./database/:/var/lib/postgresql/data
                environment:
                  - POSTGRES_USER=${PG_USER}
                  - POSTGRES_PASSWORD=${PG_PASS}
                  - POSTGRES_DB=${PG_NAME}
                healthcheck:
                  test: ['CMD-SHELL', 'pg_isready -d ${PG_NAME} -U ${PG_USER}']
                  interval: 30s
                  timeout: 60s
                  retries: 5
                  start_period: 80s
            
              server:
                build:
                  context: ./
                  dockerfile: Dockerfile
                container_name: server-1
                stop_signal: SIGKILL
                restart: always
                command: ["gunicorn", "--pythonpath", ".", "wallet_project.wsgi:application", "--bind", "0.0.0.0:8000"]
                env_file:
                  - '.env'
                ports:
                  - '8000:8000'
                healthcheck:
                  test: ['CMD-SHELL', 'curl -f http://0.0.0.0:8000/admin/ || exit 1']
                  interval: 30s
                  timeout: 10s
                  retries: 5
                  start_period: 10s
                links:
                  - database
                depends_on:
                  database:
                    condition: service_healthy
        """  # Пример файла для приложения на Python Django + PostgreSQL. # noqa
        return params, python

    @staticmethod
    def console():
        """ Тут консольные команды для docker-compose """
        commands = {
            "docker-compose --build": "Начнет собирать сеть контейнеров из файла 'docker-compose.yaml'.",
            "docker-compose up -d": "Запустит сеть контейнеров из файла в detach режиме (в фоне).",
            "docker-compose down -v": "Выключит и удалит запущенные контейнеры.",
            "docker-compose exec <name> /bin/sh": "Запустит консоль указанного контейнера.",
            "docker-compose rm": "Удаляет остановленные контейнеры для сервисов.",
            "docker-compose restart": "Перезапускает контейнеры для сервисов.",
        }
        return commands
