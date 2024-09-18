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
            "FROM python:3.10": "Задаёт базовый (родительский) образ. В данном случае Python 3.10 версии.",  # -slim-stretch - самая пустая версия с минимумом библиотек. # noqa
            "LABEL maintainer='jeffmshale@gmail.com'": "Описывает метаданные. Например — сведения о том, кто создал и поддерживает образ.",
            "COPY app.py /app/": "Копирует файлы: основная ОС -> контейнер.",
            "ARG PASS='adw14km'": "Устанавливает переменные во время сборки контейнера. К ним нельзя обращаться после сборки контейнера.",
            "ENV ADMIN='jeff'": "Устанавливает постоянные переменные. После этого к ним можно обращаться через $ADMIN даже в этом же Dockerfile.",
            "ENV PYTHONUNBUFFERED=1": "Команда возвращает логи от контейнера в консоль.",
            "ADD https://site.ru/vid1.mp4 /app": "Копирует файлы и папки в контейнер. Может распаковывать локальные .tar-файлы и работать с ссылками.",
            "EXPOSE 5000": "Открывает необходимый порт для подключения по нему к контейнеру.",
            "VOLUME /app/data": "Создает точку синхронизации Локальная ОС <-> Контейнер. docker run -v ubuntu_data/:/app/data - результат из /app/data будет в папке ubuntu_data",
            "WORKDIR /app": "В этой директории будет запущен контейнер. Уже под этой командой консоль будет работать из этой папки.",
            "RUN apt-get update && rm -rf /var/lib/apt/lists/*": "Выполняет консольную команду только при сборке контейнера(внутри него). 'RUN mkdir /app' создает папку...",
            "CMD ['python', 'app.py']": "Выполняет консольную команду только при запуске контейнера(внутри него). Если CMD/ENTRYPOINT несколько, работает только последний.",
            "ENTRYPOINT ['python', 'app.py']": "Выполняет консольную команду только при запуске контейнера(внутри него). Позволяет передавать доп. аргументы: 'docker run bla...'.",
        }

        pattern = """ Пример содержимого самого Dockerfile под приложение на Python. PYTHONUNBUFFERED=1 - вернет логи от самого приложения.
        FROM python:3.12
        ENV PYTHONUNBUFFERED=1
        RUN apt-get update && rm -rf /var/lib/apt/lists/*
        RUN mkdir /app
        COPY requirements.txt /app/
        RUN python -m pip install --no-cache-dir -r /app/requirements.txt
        COPY docs/ /app/docs/
        COPY images/ /app/images/
        COPY schemas.py /app/
        COPY models.py /app/
        COPY routes.py /app/
        WORKDIR /app
        CMD ["gunicorn", "--bind", "0.0.0.0:5000", "routes:app"] """  # noqa

        pattern_nginx = """  Шаблон контейнера для Nginx Web-сервера:
        FROM nginx

        RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
        
        COPY index.html /app/static
        COPY style.css /app/static
        COPY script.js /app/static
        
        COPY nginx.conf /etc/nginx/nginx.conf """  # noqa

        return params, pattern, pattern_nginx

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
                healthcheck:  # Тут описывает алгоритм тестирования сервиса на работоспособность.
                    test: ['CMD-SHELL', 'pg_isready -d db -U admin']  # Команда, которая тестирует статус БД. ${DB_NAME} - взять из .env данные.
                    interval: 30s  # Интервал прохождения теста.
                    timeout: 60s  # Ожидание ответа теста.
                    retries: 5  # Попыток в случае провала.
                    start_period: 80s  # ['CMD-SHELL', 'curl -f http://localhost:8000/ || exit 1'] - для Django.
                    
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
                        condition: service_healthy  # Тип проверки: сервер запущен и работает. """  # noqa
        return params

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
