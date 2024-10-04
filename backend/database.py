class SQLite:
    """ Тут расписан принцип работы с Базами Данных в стандартном стиле, приоритетно с SQLite3 """
    @staticmethod
    def classic_method():
        """ Классический метод запроса.
        conn.row_factory = sqlite3.Row - Позволяет получать результат в виде словаря
        cur.executemany(cmd, list) - применяет один запрос многократно с разными данными из списка """  # noqa
        import sqlite3

        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cur: sqlite3.Cursor = conn.cursor()

            cur.execute("SELECT id, name, age FROM 'users'")  # noqa
            for row in cur.fetchall():
                print(f"{row['id']}, {row['name']}, {row['age']}.")

            cur.execute("SELECT * FROM users WHERE id = (?)", (1,))  # 1 - поданный параметр id # noqa
            result = cur.fetchone()  # fetchone - возвращает только первый результат запроса # noqa
            conn.commit()  # Нужен для сохранения изменений в БД, например если добавилась новая запись

    @staticmethod
    def script_method():
        """ Скриптовый метод запроса """
        import sqlite3

        with open('create_schema.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        with sqlite3.connect('../database.db') as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()

    @staticmethod
    def commands():
        """ Список команд для работы с SQL таблицами. """
        commands = [
            'INSERT INTO "table_name" (name, surname) VALUES (?, ?);', (name, surname),  # INSERT INTO: Грамотно внести данные в таблицу # noqa
            'UPDATE "t1" SET value = (?) WHERE name = (?);', (value, name),  # UPDATE: обновить данные # noqa
            'DELETE FROM "t1" WHERE value = (?);', (value),  # DELETE: удалить данные # noqa
            'CREATE TABLE "t1" ("id" INT PRIMARY KEY AUTOINCREMENT, "book_id" INT, FOREIGN KEY ("book_id") REFERENCES "t2" ("id"), UNIQUE ("book_id"));',  # Большой запрос # noqa
            'CREATE OR REPLACE VIEW "name_view" AS SELECT * FROM "table_1";',  # VIEW: забиндить команду для обращения к ней по имени. DROP: удалить её # noqa
            'CREATE TABLE IF NOT EXISTS "users" (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);',  # CREATE: Создать таблицу # noqa
            'SELECT id, IIF("age" > 10, "True", "False") "result" FROM t1;',  # IIF: условный оператор сравнения # noqa
            'SELECT id, IIF(CHAR_LENGTH("name") > 10, "True", "False") "result" FROM t1;',  # CHAR_LENGTH: длина текста # noqa
            'SELECT t2.id, t1.id FROM "t1" JOIN "t2" ON t2.id = t1.id;',  # JOIN: соединение таблиц. Есть: LEFT JOIN, RIGHT JOIN, INNER JOIN, OUTER JOIN # noqa
            'SELECT t1.id, t2.id FROM t1 RIGHT JOIN t2 USING("id");',  # Выводит: все записи правой таблицы + только подходящие из левой таблицы. Равно: ON t1.id = t2.id # noqa
            'SELECT t1.id, t2.id FROM t1 INNER JOIN t2 ON t1.id > t2.id;',  # Выводит: только подходящие записи сразу правой и левой таблицы. # noqa
            'SELECT t1.id, t2.id FROM t1 LEFT OUTER JOIN t2 ON t1.id == t2.id;',  # LEFT OUTER: Выводит все значения с левой таблицы и только подходящие условию из правой # noqa
            'SELECT t1.id, t2.id FROM t1 OUTER JOIN t2 ON t1.id > t2.id;',  # OUTER: Выводит все значения, находящиеся лишь в 1 из всех таблиц # noqa
            'SELECT * FROM "t1" UNION SELECT * FROM "table_2";',  # UNION: вывести все уникальные элементы таблиц одной таблицей(объединение таблиц) # noqa
            'SELECT * FROM "t1" INTERSECT SELECT * FROM "table_2";',  # INTERSECT: пересечение 2 таблиц  # noqa
            'SELECT * FROM "table_people";'  # SELECT: Запрос всей инфы из таблицы table_people # noqa
            'SELECT * FROM "t1" WHERE "id" BETWEEN 10 AND 15;',  # BETWEEN, AND: выводит элементы в указанном диапазона # noqa
            'SELECT * FROM t1 ORDER BY stolbik DESC;',  # ORDER BY DESC: сортировка по убыванию, без DESC - по возрастанию # noqa
            'SELECT * FROM t1 GROUP BY stolbik;',  # GROUP BY: вывод уникальных значений (может использовать COUNT и т.д.) # noqa
            'SELECT * FROM t1 GROUP BY stolbik HAVING COUNT(*) >= 2;',  # HAVING: Запрос с дубликатом найденной записи # noqa
            'SELECT * FROM t1 GROUP BY stolbik LIMIT 5;',  # LIMIT: получение данных с лимитом только первые 5 элементов # noqa
            'SELECT * FROM t1 GROUP BY stolbik LIMIT 5 OFFSET 5;',  # OFFSET: получение данных со смещением на 5 элементов (то есть 5-10 элементы) # noqa
            'SELECT * FROM "t1" WHERE name LIKE "%чай%";',  # LIKE: найти в тексте выделенную часть. "%" - неограниченное кол-во символов, "_" - 1 символ # noqa
            'SELECT *, replace(stolbik, "A", "B") FROM t1;',  # REPLACE: заменить элемент в тексте A -> B # noqa
            'SELECT *, group_concat(stolbik, ",") FROM t1;',  # group_concat: при GROUP BY пихает разные строки в 1 строку. # noqa
            'SELECT CONCAT("abc", "...");',  # CONCAT: сложить строки # noqa
            'SELECT DISTINCT * FROM "t1";',  # DISTINCT: запросить уникальные элементы в таблице (не может использовать COUNT и т.д.) # noqa
            'SELECT avg(value) FROM "t1";',  # avg: запросить среднее значение суммы всех значений # noqa
            'SELECT COUNT(*) FROM "t1";',  # COUNT: запросить количество элементов из таблицы а не все элементы # noqa
            'SELECT CAST("2017-08-25" AS datetime);',  # CAST: преобразует значение в указанный тип данных # noqa
            'SELECT ROUND(avg(value), 2) FROM "t1";',  # ROUND: округляет значение # noqa
            'SELECT TRIM(name) FROM salaries;',  # TRIM: удаление лишних пробелов в строке # noqa
            'SELECT SUBSTRING("машина", 2, 3);',  # SUBSTRING: найди определенную часть текста вывод -> аши # noqa

            # Подходит для: рекурсивных, больших вложенных, частоиспользуемых, сложночитаемых запросов... Минусы: время выполнения, нагрузка на диск # noqa
            'WITH "t1" (v1, v2) AS (SELECT v1, v2 FROM "t2") SELECT * FROM "t1"',  # Создает таблицу t1 в опер. памяти, к которой можно обращаться во вложенном запросе... # noqa

            # CASE условный оператор без ограничения на количество условий
            'SELECT *, CASE WHEN "salary" > 50000 THEN "много" WHEN "salary" < 20000 THEN "мало" ELSE "нормально" END "salaryes" FROM t1;',  # Описание выше # noqa

            # Если добавляется поле: необходимо указать длину текста после названия поля. PRIMARY KEY - может даваться сразу на несколько колонок. ALTER нет в SQLite3 # noqa
            "ALTER TABLE 't1' ADD PRIMARY KEY ('id')",  # ALTER: изменяет настройки таблицы: добавить первичный ключ. Без примари - простой индекс. # noqa
            "ALTER TABLE 't1' ADD FOREIGN KEY('id') REFERENCES 't2' ('elem_id')",  # FOREIGN KEY REFERENCES: установка связи от 1 элемента к 1+ элементам # noqa
            "ALTER TABLE 't1' ADD FOREIGN KEY('id') REFERENCES 't2' ('elem_id') ON DELETE CASCADE",  # Удаляя записи в 1 таблице - удалить и во 2 таблице. Нужен ForeyignKey. # noqa
            "ALTER TABLE 't1' ADD FOREIGN KEY('id') REFERENCES 't2' ('elem_id') ON DELETE CASCADE;",  # ON DELETE: При удалении ориг. записи. CASCADE: удалит дочернюю # noqa
            "ALTER TABLE 't1' ADD FOREIGN KEY('id') REFERENCES 't2' ('elem_id') ON UPDATE SET NULL;",  # ON UPDATE: При изменении записи. SET NULL: выставит NULL на дочь # noqa
            "ALTER TABLE 't1' ADD FOREIGN KEY('id') REFERENCES 't2' ('elem_id') ON UPDATE SET DEFAULT;",  # SET DEFAULT: установит значение по умолчанию # noqa
            "ALTER TABLE 't1' ADD FOREIGN KEY('id') REFERENCES 't2' ('elem_id') ON UPDATE RESTRICT;",  # RESTRICT: Не дает менять оригинал, пока есть дочерняя ссылка на него. # noqa
            "ALTER TABLE 't1' ADD CONSTRAINT 'name_key' FOREIGN KEY ('order_id') REFERENCES 'order' ('id')",  # ADD CONSTRAINT: имя индекса внешнего ключа # noqa
            "ALTER TABLE 't1' ADD UNIQUE ('id')",  # ADD UNIQUE: установка связи от 1 элемента к 1 элементу. После нужно ADD FOREIGN KEY REFERENCES # noqa
        ]  # В других БД может немного отличаться синтаксис и некоторые команды.
        return commands


class Postgres:
    """ Тут расписана информация для работы с БД PostgreSQL """  # noqa
    @staticmethod
    def info():
        """ Тут важная информация для грамотной работы с БД, например особенности работы, защиты, миграции """
        main = """ Тут описана инструкция по работе с БД PostgreSQL и ее особенности. Стандартный порт данной БД: 5432,
        Плюсы: Объектно-реляционная СУБД, надежность, безопасность, производительность, поддержка транзакционности, бэкапы, ACID
        Плюсы над SQL, MySQL: макс. количество типов данных, система аутентификации доступа, масштабируемость, многопроцессорность, SQL совместимость, объектно-ориентированность. 
        Команды консоли PostgreSQL можно найти в классе 'Console'. """  # noqa

        acid = """ ACID: 4 свойства транзакций.
        Atomicity(Атомарность) - выражается в том, что транзакция должна быть выполнена в целом или не выполнена вовсе.

        Consistency(Согласованность) - гарантирует, что по мере выполнения транзакций, данные переходят из одного согласованного состояния в 
        другое, то есть транзакция не может разрушить взаимной согласованности данных.

        Isolations(Изолированность) - локализация пользовательских процессов означает, что конкурирующие за доступ к БД транзакции физически 
        обрабатываются последовательно, изолированно друг от друга, но для пользователей это выглядит, как будто они выполняются параллельно.

        Durability(Долговечность) - устойчивость к ошибкам — если транзакция завершена успешно, то те изменения в данных, которые были ею 
        произведены, не могут быть потеряны ни при каких обстоятельствах.
        """  # noqa

        isolation = """ Уровни изоляции и режимы работы БД в отношении к ним.
        Всего есть 4 уровня изоляции (Для выбора нужного уровня изоляции транзакций используется команда SET TRANSACTION):
            1 «грязное» чтение - Транзакция читает данные, записанные параллельной незавершённой транзакцией.
            2 неповторяемое чтение - Транзакция повторно читает те же данные, что и раньше, и обнаруживает, что они были изменены другой транзакцией 
                (которая завершилась после первого чтения).
            3 фантомное чтение - Транзакция повторно выполняет запрос, вернувший набор строк для условия, и видит, что набор строк для условия - изменился из-за 
                транзакции, завершившейся за это время.
            4 аномалия сериализации - Результат успешной фиксации группы транзакций оказывается несогласованным при всевозможных вариантах исполнения этих транзакций по очереди.

        Режимы работы БД с уровнями изоляции:
            Read uncommited (Чтение незафиксированных данных) mode.
                Статусы: 1 не поддерживается в PG базе данных, 2, 3, 4 состояния поддерживаются.
                Работа: При создании 1+ соединений к БД в этом режиме если транзакция А изменит какие то данные, то изменения будут видны всем транзакциям(А, Б, В...) до коммита.

            Read committed (Чтение зафиксированных данных) mode(default в PostgreSQL).
                Статусы: поддерживаются только 2, 3, 4 состояния.
                Работа: При создании 1+ соединений к БД в этом режиме если транзакция А изменит какие то данные, то изменения будут видны ей одной, транзакции Б, В... будут 
                    видеть устаревшие данные до тех пор, пока транзакция А не закоммитит изменения.

            Repeatable read (Повторяемое чтение) mode.
                Статусы: 3 не поддерживается в PG базе данных, 4 состояние поддерживается.
                Работа: Транзакции видят только данные, которые были считаны на момент начала транзакции. он никогда не видит ни незафиксированные данные, ни 
                    изменения, зафиксированные во время выполнения транзакции параллельными транзакциями. (Однако запрос видит последствия предыдущих 
                    обновлений, выполненных в рамках его собственной транзакции, даже если они еще не зафиксированы.)
                Пример: Транзакция А использует SELECT и получает 2 строки, транзакция Б использует INSERT и добавляет строку (теперь их 3), транзакция А повторно 
                    использует SELECT и получает снова 2 строки, без 3.

            Serializable (Сериализуемость) mode.
                Статусы: НЕ поддерживает состояния 1, 2, 3, 4.
                Работа: При создании 1+ соединений к БД в этом режиме если транзакция А изменит какие то данные, то изменения будут видны только ей, транзакции Б, В... не 
                    смогут видеть эти изменения, и не смогут повлять на эти же измененные данные, в случае попытки изменения транзакции зависнут до завершения 
                    транзакции А, а после ее завершения получат ошибку и откатят все свои изменения. Так же даже после того, как транзакция А закоммитит 
                    изменения, они все равно не смогут увидеть изменения, их придется повторно перезапускать.
                Пример:
                     class | value
                    -------+-------
                         1 |    10
                         1 |    20
                         2 |   100
                         2 |   200
                    -------+-------
                    транзакция A вычисляет: SELECT SUM(value) FROM mytab WHERE class = 1;
                    транзакция B вычисляет(асинхронно): SELECT SUM(value) FROM mytab WHERE class = 2;
                    Транзакция B получает результат 300 и вставляет его в новую строку со значением class = 1. Затем обе транзакции пытаются 
                    зафиксируются. В режиме Serializable будет зафиксирована только одна транзакция, а вторая закончится откатом.
                    Это объясняется тем, что при выполнении A перед B транзакция B вычислила бы сумму 330, а не 300, а при выполнении их 
                    в обратном порядке A вычислила бы другую сумму.
                    На практике такой уровень изоляции требуется в учетных системах.
        """  # noqa

        transaction = """ 
        Пример открытия транзакции и выполнения в ней нескольких команд:
            BEGIN SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE NOT DEFERRABLE;
            SELECT...
            INSERT...
            DELETE...;
            COMMIT; 

        BEGIN - означает начало транзакции, все что между ней и commit будет работать в пределах этой транзакции (аналог в SQL: START TRANSACTION), в SQL 
            слово BEGIN имеет другие значения, надо быть аккуратным. Используйте COMMIT или ROLLBACK для завершения блока транзакции.

        Шаблон установки уровня изоляции выглядит следующим образом:
        SET TRANSACTION ISOLATION LEVEL {SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED} {READ WRITE | READ ONLY} [NOT] DEFERRABLE, где
            1) SET TRANSACTION - установка настроек транзакции.
            2) ISOLATION LEVEL - установка уровня изоляции (одного из указанных).
            3) READ WRITE or READ ONLY - режим чтения/записи.
            4) DEFERRABLE - Этот режим хорошо подходит для длительных отчетов или резервного копирования. Отключает сбой сериализации или отката изменений (только PostgreSQL). 

        Так же можно начать новую транзакцию со снимком данных, который получила уже существующая транзакция, его нужно сначала экспортировать из первой транзакции 
        командой 'SET TRANSACTION SNAPSHOT id_снимка' (только PostgreSQL):
            1) Получаем идентификатор из первой транзакции:
                BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
                SELECT pg_export_snapshot();
                pg_export_snapshot
            # Возвращает что то типа: 000003A1-1

            2) Используем идентификатор во второй транзакции:
                BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
                SET TRANSACTION SNAPSHOT '000003A1-1';

        Пример создания сессии с контрольной точкой и откатом:
            with engine.connect() as conn:  # Создает соединение с датабазой. Работа с датабазой через connection. # noqa
                with conn.begin():  # Играет роль conn.commit(), следовательно вручную комитить не нужно. Область запросов, так же создает транзакцию # noqa
                    transaction = session.begin_nested()  # Создает контрольную точку транзакции (начало транзакции) # noqa
                    transaction.rollback()  # Откатывает транзакцию до контрольной точки
        """  # noqa

        extension = """ extension - расширение. Расширение PostgreSQL обычно включает в себя несколько объектов SQL; например, новый тип данных потребует новых 
        функций, новых операторов и, возможно, новых классов индексных операторов. Полезно собрать все эти объекты в один пакет, чтобы упростить управление базой данных.

        Посмотреть список стандартных расширений: 'SELECT * FROM pg_available_extensions'

        Установка любых расширений: CREATE EXTENSION IF NOT EXISTS extension_name WITH SCHEMA schema_name VERSION version CASCADE, где
            WITH SCHEMA: имя схемы, для которой будет произведена установка. Если не указано, то установится в текущую схему.
            VERSION: версия для установки. Если не указано, то будет установлена последняя.
            CASCADE: автоматическая установка всех дополнительных расширений, необходимых для работы.
            После установки с помощью этой команды требуется внести определенные записи в файл конфигурации PostgreSQL, а потом перезапустить сервер.

        Так же можно обновить или удалить расширение соответственно:
            ALTER EXTENSION extension_name UPDATE TO version # Если не указать параметр version, будет установлена последняя версия.
            DROP EXTENSION IF EXISTS extension_name {CASCADE | RESTRICT} # CASCADE: удалить все, что зависит от расширения. RESTRICT: не удалять, если от него что то зависит.

        Доп. примеры:
            DROP EXTENSION hstore;
            CREATE EXTENSION hstore SCHEMA public FROM unpackaged;
            DROP EXTENSION [IF EXISTS] name [, ...] [CASCADE | RESTRICT]
            CREATE EXTENSION [IF NOT EXISTS] extension_name [WITH] [SCHEMA schema_name] [VERSION version] [FROM old_version]
            extension_name - Имя устанавливаемого расширения. PostgreSQL создаст расширение, используя данные из файла SHAREDIR /extension/ extension_name.control
        """  # noqa

        loads = """ Тут примеры загрузки данных в асинхронном режиме (нужны, что бы можно было обращаться к атрибутам через '.' например user.id):
        Вариант через relationship(прямо в создании таблицы):
            addresses = relationship("Address", back_populates="user", lazy="selectin") # lazy=selectin - загружает инфу, позволяя к ней обращаться как table.addresses

        Вариант при составлении запроса:
            for user_obj in session.execute(select(User).options(selectinload(User.addresses))).scalars():
                user_obj.addresses # selectinload(user.addresses) - загружает инфу, позволяя к ней обращаться

        Так же надо вручную обновлять объекты в памяти:
            q = update(Product).where(Product.id == product_id)
            q.execute_options(synchronize_session='fetch')
        """  # noqa

        return main, acid, isolation, transaction, extension, loads

    @staticmethod
    def start_work():
        """ Тут способы запуска PostgreSQL. Сперва нужно стянуть образ БД с докера: docker pull postgres, потом уже запускать.
        Основные методы запуска: docker-container, docker-compose.yaml файл. """  # noqa

        docker_container = """ Запуск PostgreSQL через docker-container: 
        docker run --name <name_cont> --rm -e POSTGRES_USER=postgres -e POSTGRES_PASS=postgres 
        -e PGDATA=/var/lib/postgresql/data/pgdata -v /tmp:/var/lib/postgresql/data/pgdata -p 5432:5432 -it postgres,
            --name <name_cont> - Имя контейнера
            -e - передача переменных, в данном случае логин, пароль, место хранения бд, кэш файлы
            -p - порт ввода:вывода взаимодействия с БД
            -it - интерактивный режим, типа запуск в свернутом виде без лишней информации.

        Команды для консоли, с помощью которых можно взаимодействовать с запущенным docker-container БД:
            docker exec -it <name_cont> /bin/sh # Команда для запуска в запущенном контейнере консоли
            psql -U postgres # Команда для подключения БД через пользователя POSTGRES_USER=postgres
        """  # noqa

        docker_compose_yaml = """ Запуск PostgreSQL через docker-compose.yaml файл. Структура файла:
        version: '3.9' # Версия docker-compose
        services:
          postgres: # Адресс для обращения к БД, типа IP при подключении внутри docker-сети, если подключаться не в docker-сети, то дефолт localhost или реальный IP
            image: postgres # Скачанный с помощью docker pull образ БД
            user: 1000:1000 # sudo chown -R 1000:1000 ./db # если нет прав на папку с БД. Удалить строку если не нужна
            environment: # Переменные окружения
              - POSTGRES_USER=admin
              - POSTGRES_PASSWORD=admin
            ports: # Порт ввода:вывода
              - '5432:5432'
            volumes: # Временные файлы. /var/lib/postgresql/data - БД внутри докера, после чего данные синхронизируются с ./db/ локальной машины, где хранят данные вне докера.
              - ./db/:/var/lib/postgresql/data

        Запуск: docker-compose up или docker compose up(старые версии).
        Команды для консоли, с помощью которых можно взаимодействовать с запущенным docker-compose.yaml файлом БД:
            docker exec -it <name_cont> /bin/sh # Команда для запуска в запущенном контейнере консоли
            psql -U postgres # Команда для подключения БД через пользователя POSTGRES_USER=postgres
        """  # noqa

        return docker_container, docker_compose_yaml

    @staticmethod
    def migrations():
        """ Миграция - процесс обновления версии БД, требует: атомарность, упорядоченность, обратимость. Упорядоченность(пример) - создание новой 
        колонки, а уже потом добавление нового индекса """  # noqa

        yoyo = """ Тут описан инструмент для миграции БД PostgreSQL - pip install yoyo-migrations
        Достоинства:
            1) Структурированные файлы с изменениями БД
            2) Фиксация миграций в отдельной таблице _yoyo_migration
            3) Выполнение каждой миграции в отдельной транзакции
            4) Проверка возможности выполнения транзакции

        Минусы:
            1) Ручное написание запросов на чистом SQL

        Команды для консоли, в которых можно работать с yoyo-migrations:
            yoyo new ./migrations -m 'add column to product' # создает папку для хранения миграций и открывает редактор vim

        Первая команда для обновления БД, вторая для отката если их много - пишутся через запятую: step("..."), step("...")...
        Внутри step("") пишутся нужные SQL команды, например:
            step("ALTER TABLE products ADD column color varchar(100)", "ALTER TABLE products DROP column color") 

        Выход из vim: esc - :x - сохранить и выйти.

        Подключение yoyo к БД:
            через yoyo.ini: database = postgresql//admin:admin@localhost # тогда запуск в консоли: yoyo apply
            через консоль: yoyo apply --database postgresql://admin:admin@localhost/db ./migrations

        Откат миграции: yoyo rollback """  # noqa

        alembic = """ Тут описаны миграции на pip install alembic
        Достоинства:
            1) Простое внедрение, реализован для SQLAlchemy
            2) Автоматическая генерация кода генераций на основе ORM-моделей
            3) Возможность использования python-функций внутри кода миграций
            4) Фиксация миграций в отдельной таблице alembic_version

        Минусы:
            1) Миграции не фиксируют изменения имени таблиц и колонок

        Начало работы с alembic:
            1) alembic init alembic в консоли в нужной дирректории, работает аналогично git init
            2) в alembic.ini указать драйвер БД от SQLAlchemy: postgresql://admin:admin@localhost # пример
            3) в alembic.ini указать путь до дирректории приложения, откуда надо импортировать metadata дальше (application папка)
            4) в env.py нужно указать target_metadata = Base.metadata из нашей БД
            5) Создается контрольная точка alembic в консоли: alembic revision --message="init migration" --autogenerate

        При работе из докера может потребоваться еще ввести: alembic stamp head # значит, что текущее состояние базы данных представляет собой применение всех миграций.

        Обновить миграцию: alembic upgrade head # функция upgrade в созданной миграции в папке.
        Откатить миграцию: alembic downgrade head # Функция downgrade в созданной миграции в папке.
            head можно менять на идентификатор версии БД. Пример alembic downgrade adjkwn12adiw-1 # -1 значит на состояние перед этой миграцией

        Что бы посмотреть чистые SQL запросы, нужно в alembic.ini и включить revision_environment = True
        Если 2 разраба параллельно заливают миграцию, можно напороться на ошибку по их сложению, для решения:
            1) alembic merge heads -m "merge code bla bla" # совмещает 2 миграции и создает одну новую единую
            2) alembic upgrade head # завершающая миграция двух проблемных миграций
        """  # noqa

        return yoyo, alembic

    @staticmethod
    def console():
        """ БД запускается через Docker, далее к ней нужно подключиться: docker exec -it <container> /bin/sh
        Далее авторизация в БД: psql -U <name>:<pass> и уже потом можно работать с БД изнутри. """  # noqa

        commands = {
            "\l": "Список доступных БД",  # noqa
            "\c <name>": "Подключиться к существующей БД по имени",  # noqa
            "CREATE DATABASE name;": "Создает базу данных из консоли PostgreSQL",  # noqa
            "\dx": "Посмотреть список доступных расширений",  # noqa
            "\dt": "Список таблиц в активной БД",  # noqa
            "exit": "В консоли БД вернуться на прошлый уровень работы",
            "=======": "Команды уже для таблиц по большей части",
            "SELECT * FROM pg_extension;": "Посмотреть список доступных расширений",  # noqa
            "SELECT * FROM pg_available_extensions": "Посмотреть список стандартных расширений",  # noqa
            "BEGIN SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE NOT DEFERRABLE;": "Открытие транзакции с указанными параметрами",  # noqa
            "SELECT pg_export_snapshot(); pg_export_snapshot": "Отдает скриншот считанных данных для передачи в другую транзакцию в таком же виде",
            "SET TRANSACTION SNAPSHOT '000003A1-1';": "Загружает скриншот считанных данных из другой транзакции",
            "CREATE EXTENSION IF NOT EXISTS ext_name WITH SCHEMA schema_name VERSION version CASCADE": "Создает расширение с указанными параметрами",  # noqa
            "ALTER EXTENSION extension_name UPDATE TO version": "Обновление существующего расширения",  # noqa
            "DROP EXTENSION IF EXISTS extension_name {CASCADE | RESTRICT}": "Удаление существующего расширения",  # noqa
            "ALTER TABLE 't1' ADD PRIMARY KEY ('id')": "Обновление самой таблицы: добавить первичный ключ",  # noqa
        }  # Консольные команды. # noqa
        return commands


class SQLAlchemy:
    """ Тут расписано все, что касается работы с Базами Данных через ORM. Пара советов безопасности:
    1. Использовать session.execute(), т.к. он выполняет скрипт только до первого символа ';'.
    2. Подставлять данные не на прямую, а через (?) переменные. """
    @staticmethod
    def information():
        """ Тут работа с БД на ORM (Аддон, позволяющий работать с кодом языка SQL как с кодом конкретного языка программирования, в данном случае Python). 
        session.flush() - передает измененные данные в БД, но не коммитит их, т.е. надо ждать коммит (он всегда вызывается внутри commit(), так же 
        в session есть autoflush=True """  # noqa

        database_url = """ Работа с БД на ORM SQLAlchemy. URL для подключения к БД составляется следующим образом:
        dialect+driver://username:password@host:port/database - образец подключения к БД, где:
            dialect - название Базы данных.
            driver - используемый DBAPI(необязательно), если его не указать будет использоваться по умолчанию (если он установлен, например SQLite3).
            username - Логин для подключения, может быть зарегистрирован учетной записью в БД, или подаваться как переменная окружения в docker, например POSTGRES_USER=admin.
            password - Пароль для подключения, может быть зарегистрирован учетной записью в БД, или подаваться как переменная окружения в docker, например POSTGRES_PASSWORD=admin.
            host - Расположение сервера базы данных. Например localhost для своего ПК или IP адрес удаленного сервера, или имя в docker-сети (например 'postgres').
            port - Порт для подключения. Можно не указывать. В PostgreSQL по умолчанию 5432.
            database - название БД для работы, может быть файлом типа 'db.db' или простым названием в БД PostgreSQL (Расширение .db указывать не обязательно). """  # noqa

        foreignkey_obj = """ from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
        ForeignKey - первичный ключ, создающий связь между двумя таблицами. Обязательная базовая штука, которая позволяет связать таблицы изначально, после чего уже 
            настраивать эту связь. 
        Изначально SQLAlchemy не может работать с несколькими ForeignKey сразу. Сама связь создается по такому принципу:
            1) Главная таблица, ключ ForeignKey ставится на PrimaryKey. Точнее это значение указывается при настройке самого ключа(Т.е. при настройке указывается 
                ссылка на primary_key таблицы, на которую ключ будет ссылаться).
            2) Вторая таблица создает себе колонку-ссылку на первую таблицу. ForeignKey('table.column') - где table - таблица, на которую ссылается, column - колонка 
                с primary_key этой таблицы. Для себя же создает свою колонку для ссылки на другую. 
                Итоговый пример выглядит так во второй таблице: user_id: Mapped[int] = mapped_column(ForeignKey("users.id")).

        Constraint - Это по сути ключи, которые дописывают настройки на уровне таблицы, например могут модернизировать колонку на primary_key, если он не установлен 
            в этой колонке. Важно, что это описывается на уровне таблицы, т.е. например __table_args__ = (UniqueConstraint("user_id"),) делает user_id колонку 
            с unique=True, так же Constraint учит SQLAlchemy работать сразу с несколькими ForeignKey в таблице:
                1) ForeignKeyConstraint - По сути просто превращает конкретную колонку в ForeignKey. 
                2) UniqueConstraint - Превращает колонку в unique=True значение.
                3) PrimaryKeyConstraint - Превращает в primary_key=True.
                4) CheckConstraint - Позволяет добавить custom проверку поля, 
                    например: CheckConstraint('salary < 100000', name='salary_check'), salary - колонка, salary_check - результат проверки.

        Важным замечанием тут будет тот факт, что через Constraint можно удобно настраивать сразу несколько ключей, что очень удобно, если 1 таблица ссылается 
            сразу на несколько других таблиц (например таблица связи many_to_many).

        Так же в ForeignKey можно указать параметры onupdate и ondelete. Пример: Annotated[int, mapped_column(ForeignKey("users.id", onupdate="SET NULL", ondelete="CASCADE"))]. 
            Этот параметр можно более гибко настроить внутри relationship связей, например: relationship("Child", cascade="all,delete", backref="parent"). """  # noqa

        relationship_obj = """ from sqlalchemy.orm import relationship
        relationship - хранилище ссылок на дочерние элементы, т.е. обеспечивает связь между таблицами, аргументом принимает дочерняя таблица. 
        В именованных ключах есть 2 аргумента:
            1) back_populates="first" - Указывает связь на дочернюю таблицу на специфичную колонку 'first' для связи. Для двунаправленной связи требует указать и у 
                дочерней таблицы такую же строку и колонку в первой таблице, на которую он сможет ссылаться (Например: back_populates="second" - second колонка в 
                первой таблице, на которую будет ссылаться уже вторая таблица, в общем то же самое только наоборот). По сути back_populates - создает строго 
                одностороннюю связь, поэтому если в 2 таблицах сделать по односторонней связи, то получится двусторонняя.
                Пример: first: Mapped["User"] = relationship(back_populates="second"), где first - ссылка в одной таблице, а second ссылается на таблицу User, столбик second.

            2) backref="first" - Тоже самое, что и back_populates, но уже создает строго двустороннюю связь, благодаря чему во второй таблице не нужно указывать дубликат 
                записи со своей колонкой, ведь она создается сама. Значение 'first' указывает название колонки, которую ORM сама создаст во второй таблице для настройки связи.
                Пример: first: Mapped["User"] = relationship(backref="second"), где first - ссылка в одной таблице, а second - столбик, который сам создастся в 
                    таблице User и будет обратной ссылкой.

        Так же в relationship можно установить более тонкое каскадное поведение, например: relationship("Child", cascade="all, delete-orphan", backref="parent"), однако 
        стоит подметить, что это работает строго с session.delete() методом. Основные параметры:
            1) all - Заключает в себе все настройки, кроме delete-orphan. Однако их можно указать вместе через запятую.
            2) delete-orphan - При удалении родителя удаляет и дочерние элементы(даже не загруженные с ним в session). Вместе с all они удаляют все.
            3) delete - При удалении родителя удаляет и дочерние элементы(но только загруженные с ним в session).
            4) save-update - При запросе родителя, загрузит сразу и дочерние элементы(типа вместе с User все его Address, НО не на оборот). 
                При удалении объекта в одной сессии и добавлении в другой глючит.

        Так же в relationship можно установить алгоритм загрузки данных с помощью параметра lazy, например: relationship("Child", lazy="selectin", backref="parent"). 
        Основные параметры:
            1) lazy - При запросе объекты загружаются без связанных таблиц, связанные загружаются при их использовании.
            2) eager - При запросе объекты загружаются со связанными объектами.
            3) no loading - Отключение загрузки для связанных таблиц.
            4) raise - При запросе объектов из связанной таблицы выкидывается исключение. """  # noqa

        onupdate_ondelete = {  # onupdate и ondelete параметры - указывают поведение элемента при изменении родительского объекта. Указываются на ForeignKey. # noqa
            "Функция": "Может указываться любая функция. Например при обновлении установить параметр 'datetime.now' и время будет обновляться при изменении родителя.",
            "CASCADE": "При обновлении или удалении родителя будут удалены дочерние записи.",
            "DELETE": "",
            "RESTRICT": "При обновлении или удалении родителя, если есть дочерние связи, то выдаст ошибку и отменит операцию.",
            "SET NULL": "При обновлении или удалении родителя будет установлено значение 'NULL'.",
        }

        cascade = {  # CASCADE параметры указывают поведение при изменении или удалении дочерних и родительских данных. Часто нужен при создании связей.
            "all": "Все, кроме delete-orphan, однако его можно добавить через запятую.",
            "delete-orphan": "Удаляет записи, если их родитель или ребенок пропадает.",
            "delete": "Если родитель удаляется, то удаляются и дочерние элементы.",
            "save-update": "Позволяет автоматически подгружать дочерние элементы к записи, которую мы загружаем в сессию.",
        }

        lazy = {  # LAZY параметры указывают, как сессия должна загружать данные, например связи. Часто нужен для связей и асинхронных подключений.
            "select (значение по умолчанию)": "Будет загружать данные по мере необходимости в один заход с использованием стандартного оператора выбора.",
            "immediate": "При вызове источника отношения также вызывается пункт назначения отношения. В общем урезанная версия selectin.",  # noqa
            "selectin": "Загружаются все члены связанных коллекций/скалярных ссылок. сразу по первичному ключу.",  # noqa
            "joined": "Будет загружать связи в том же запросе, что и родительский, используя оператор JOIN.",
            "subquery": "Работает как «joined», но использует подзапрос (выполняется при каждом запросе в на данные, что плохо при поиске кучи соответствий в 1 запросе).",  # noqa
            "dynamic": "Вместо того чтобы загружать элементы, SQLAlchemy будет возвращать объект запроса, который можно дополнительно уточнить перед загрузкой элементов.",
            "raise": "Запускается одновременно с ленивой загрузкой, за исключением того, что она вызывает исключение ORM для защиты от нежелательных ленивых загрузок приложения.",
            "write_only": "Загруженный объект можно изменять, но его данные не будут загружены в память.",
            "noload": "Не будет загружать, этот аттрибут будет просто пустым."
        }
        return database_url, foreignkey_obj, relationship_obj, onupdate_ondelete, cascade, lazy

    @staticmethod
    def database_urls():
        """ Основные подключения к БД. """
        DATABASE_URL = "sqlite+sqlite3:///data.db"  # Синхронное подключение к локальной базе данных. # noqa
        DATABASE_URL = "sqlite+aiosqlite:///data.db"  # Асинхронное подключение к локальной базе данных. Нужно: 'pip install aiosqlite'. # noqa
        DATABASE_URL = "postgresql+psycopg2://login:password@ip:5432/db"  # Синхронное подключение к PostgreSQL, pip install psycopg2-binary # noqa
        DATABASE_URL = "postgresql+asyncpg://login:password@ip:5432/db"  # Асинхронное подключение к PostgreSQL, pip install asyncpg # noqa

    @staticmethod
    def sync_implement_database():
        """ Тут расписана синхронная работа с БД. Классический стиль описания таблиц. Особенность: сперва описывается класс Table(), потом по нему создаются модели с логикой... """
        from sqlalchemy import create_engine  # noqa
        from sqlalchemy.orm import sessionmaker  # noqa

        engine = create_engine(DATABASE_URL)  # noqa
        session_obj = sessionmaker(bind=engine, expire_on_commit=False)
        session = session_obj()  # noqa

        from sqlalchemy import MetaData, Table, Column, Integer, String, Sequence, ForeignKey  # noqa
        from sqlalchemy.orm import mapper, relationship  # noqa

        metadata = MetaData(bind=engine)  # Класс, который хранит в себе описание таблиц # noqa

        users = Table(  # Класс грамотного описания таблицы users. Хранит в себе только информацию объекта (без логики)
            "users",  # Название таблицы - users
            metadata,  # класс хранения таблицы
            Column("id", Integer, Sequence("user_id_seq"), primary_key=True),  # Sequence - генерирует нумерацию, надо для primary key # noqa
            Column("name", String(50))
        )  # в String важно указывать длину для избежания лишних ошибок

        class User:  # Класс логики объекта, В нем описываются методы запросов и т.д. # noqa
            def __init__(self, name):  # В класс подаются только значения, которые НЕ заполняются автоматически в таблице (например autoincrement'ом). Не обязательный метод # noqa
                self.name = name

            def __repr__(self):  # Оператор repr вызывает при использовании print(). Не обязательный метод # noqa
                return f'{self.name}'

        addresses = Table(
            "addresses",
            metadata,
            Column("id", Integer, Sequence("address_id_seq"), primary_key=True),
            Column("user_id", None, ForeignKey("users.id")),  # не указывается тип данных, потому-что ссылается на конкретный тип (таблица users - id - это integer) # noqa
            Column("email_address", String(100), nullable=False)
        )  # nullable - может ли быть строка пустой

        class Address:  # Класс логики объекта, Аналогично классу User # noqa
            pass

        mapper(User, users)  # Связывает класс логики и класс информации объекта. Позволяет в итоге расширить функционал # noqa
        mapper(users, properties={'addresses': relationship(addresses)})  # Устанавливает связь 1 ко многим в класическом стиле описания таблиц # noqa
        metadata.create_all(bind=engine, checkfirst=True)  # Проверяет есть ли таблицы в датабазе, если нет - создает указанные в metadata. # noqa

    @staticmethod
    def async_declarative_database():
        """ Тут расписана асинхронная работа с БД. Декларативный стиль описания таблиц. Особенность: логика и класс информации пишутся уже вместе. Современный синтаксис. """
        import asyncio
        from typing import Dict, List, AsyncGenerator
        from typing_extensions import Annotated
        from sqlalchemy import ForeignKey, UniqueConstraint, Table, Column, select, insert, update, delete, func, and_  # noqa
        from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, MappedAsDataclass  # noqa
        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine  # noqa
        from sqlalchemy.ext.declarative import declarative_base  # noqa

        Base = declarative_base()  # noqa
        async_engine = create_async_engine(DATABASE_URL)  # noqa
        async_maker = async_sessionmaker(
            bind=async_engine, class_=AsyncSession, expire_on_commit=False
        )  # expire_on_commit - истечение срока действия объекта после коммита. # noqa

        # Принцип составления аннотаций типов в современном стиле. Применение: id: Mapped[str_unique], а это: = relationship(...) можно уже в самой таблице.
        user_fkey_unique = Annotated[int, mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)]  # noqa
        str_unique = Annotated[str, mapped_column(unique=True)]  # noqa

        async def get_async_session() -> AsyncGenerator[AsyncSession, None]:  # noqa
            """ Функция создает и отдает асинхронную сессию """
            async with async_maker() as session:
                yield session

        class Universal(Base):  # Универсальный класс, от которого наследуются остальные и сразу имеют одинаковые колонки id. # noqa
            """ Класс, который хранит в себе общие признаки всех таблиц """
            __abstract__ = True  # Нужно, что бы этот класс не создавал таблицу в базе данных для себя.
            __allow_unmapped__ = True  # Нужна для аннотаций под mypy в старых версиях (до SQLAlchemy 2.0).

            id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, init=False)  # init - значение создается при __init__ класса. # noqa

            @classmethod
            @declared_attr  # noqa
            def __tablename__(cls) -> str:  # Название таблицы = названию класса в нижнем регистре. Заменяет: __tablename__ = "user", и ее можно удалить # noqa
                return cls.__name__.lower()

            def to_json(self) -> Dict[str, Any]:  # Возвращает запись из таблицы в виде словаря # noqa
                return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # noqa

        class User(Universal):  # Таблица для примеров. # noqa
            """ Рабочий класс пользователя. Опасные запросы рекомендуется делать через 'session.execute(...)', т.к. он выполняет только 1 запрос до ';'. """
            __tablename__ = "users"  # Название таблицы. # noqa
            __table_args__ = ""  # Атрибут для конфигурации объекта Table(). Например: (UniqueConstraint("email_id"),) # noqa
            __mapper_args__ = ""  # Атрибут для конфигурации объекта mapper(). Тоже, что и выше, например: {"schema": "ItemSchema"} # noqa

            name: Mapped[str_unique]  # = relationship(...) по необходимости. # noqa
            age: Mapped[int]

            @staticmethod
            async def select_methods(user_id: int = 1, session: AsyncSession = get_async_session()):  # noqa
                """ В этой функции примеры использования запросов для выборки элементов. """
                stmt1 = select(User).where(User.id == user_id)  # noqa
                result = await session.execute(stmt1)  # Возвращаемые типы: .fetchall() - список коллекций | .fetchone() - коллекция. # noqa
                return result.fetchone()  # .scalar() - класс | .scalars().all() - список классов | .scalars().first() - первый найденный класс. # noqa

            @staticmethod
            async def update_methods(name: str = 'name', age: int = 18, session: AsyncSession = get_async_session()):  # noqa
                """ В этой функции примеры использования потенциально опасных запросов к базе данных. """
                stmt1 = insert(User).values(name=name, age=age).returning(User)  # noqa
                stmt2 = update(User).values(age=age).returning(User).where(User.name == name)  # noqa
                stmt3 = delete(User).returning(User).where(and_(User.name == name, User.age == age))  # noqa
                result = await session.execute(stmt1)
                await session.commit()  # Возвращаемые типы: .fetchall() - список коллекций | .fetchone() - коллекция. # noqa
                return result.fetchone()  # .scalar() - класс | .scalars().all() - список классов | .scalars().first() - первый найденный класс. # noqa

            @staticmethod
            async def bulk_methods(session: AsyncSession = get_async_session()):  # noqa
                """ В этой функции примеры использования массовых запросов к базе данных. """
                async with session.begin():  # То же самое, что и 'await session.commit()', только лучше.
                    await session.bulk_save_objects([User(name="kolya", age=4), User(name="petya", age=5)])  # Если они уже в таблице, вызывается UPDATE. # noqa
                    await session.bulk_insert_mappings(User, [{"name": "kolya", "age": 5}, {"name": "petya", "age": 6}])  # noqa
                    await session.bulk_update_mappings(User, [{"id": 1, "name": "kolya"}, {"id": 2, "name": "petya"}])  # noqa

            @staticmethod
            async def subquery_methods(session: AsyncSession = get_async_session()):
                """ В этой функции пример использования вложенного запроса в другом запросе к базе данных. """
                support = select(func.max(User.age)).select_from(User).subquery()  # Вернет максимальный возраст среди пользователей. # noqa
                stmt = select(User.id).where(User.age == support)  # select_from - для поиска из вспомогательного запроса. # noqa
                result = await session.execute(stmt)
                return result.fetchone()

            @staticmethod
            async def another_methods(session: AsyncSession = get_async_session()):
                """ В этой функции показано еще несколько примеров различных фишек. """
                User.id.label('user_id')  # При возвращении результатов заменяет название колонки. # noqa

                ins = insert(Product).values(id='2', title='новый продукт')  # Для примера ниже # noqa
                do_nothing = ins.on_conflict_do_nothing(index_elements=['id'])  # При конфликте ничего не делать # noqa
                do_update = ins.on_conflict_do_update(constraint='products_pkey', set_=dict(title='обновленный продукт'))  # При конфликте заменяет данные # noqa

                user = session.execute(select(User).where(User.id == 1)).fetchone()  # Добавление новой связи для объекта. # noqa
                character = session.execute(select(Character).where(Character.id == 1)).fetchone()  # noqa
                user.one_to_more.append(character)  # Примерная схема добавления связи. Для списка: '.extend([my_mail, my_mail2...])'. # noqa

        async def relationships():  # Примеры составления различных связей между таблицами. # noqa
            """ Для самой связи достаточно, что бы был указан ForeignKey, он обеспечит соединение всех данных, вручную в список child ничего не нужно добавлять. """
            fku = Annotated[int, mapped_column(ForeignKey("first.id"), unique=True, nullable=False, onupdate="SET NULL")]  # unique, потому-что связь строго 1к1. # noqa
            fk = Annotated[int, mapped_column(ForeignKey("first.id"), nullable=False, onupdate="SET NULL")]  # уже не unique, потому-что связь 1к9. # noqa

            class First(Universal):  # noqa
                __tablename__ = "firsts"  # noqa
                oto1: Mapped["Second"] = relationship("Second", backref="oto2", uselist=False, cascade="delete", lazy="joined")  # Связь 1к1. # noqa
                otm1: Mapped[List["Second"]] = relationship("Second", backref="otm2", uselist=True, cascade="delete", lazy="selectin")  # Связь 1к9. # noqa

            class Second(Universal):  # noqa
                __tablename__ = "seconds"  # noqa
                oto_fku = Mapped[fku]  # Связь 1к1. Обязательно должен быть уникальным, что бы несколько таких записей не ссылались на 1. # noqa
                # oto2: Mapped["First"] = relationship("First", back_populates="oto1")  # Строка нужна только если child сделан через back_populates для обратной связи. # noqa
                otm_fk: Mapped[fk]  # Связь 1к9. Тут уже ForeignKey не должен быть уникальным. # noqa
                # otm2: Mapped["First"] = relationship("First", back_populates="otm1")  # Строка нужна только если otm1 сделан через back_populates для обратной связи. # noqa

            def many_to_many():  # noqa
                """ Связь многие ко многим. Главное отличие - дополнительная таблица для хранения связей и первичными ключами к двум основным связываемым таблицам.
                Так же в каждой таблице нужно прописывать связь отдельно через back_populates, а так же надо добавлять связь вручную, вот так: 'obj1.child.append(obj2)'. """
                def two_tables():  # noqa
                    """ Тут описана связь многие-ко-многим между двумя разными таблицами. В основных таблицах ForeignKey уже не нужны, они в таблице ассоциации. """
                    association = Table("associations", Base.metadata,  # noqa
                        Column("user_id", ForeignKey("users.id"), primary_key=True),  # onupdate и ondelete можно настроить по усмотрению # noqa
                        Column("address_id", ForeignKey("addresses.id"), primary_key=True),
                    )

                    class User(Base):  # noqa
                        __tablename__ = "users"
                        child: Mapped[List["Address"]] = relationship(secondary=association, back_populates="parent", uselist=True, lazy="selectin", cascade="delete")

                    class Address(Base):  # noqa
                        __tablename__ = "addresses"
                        parent: Mapped[List["User"]] = relationship(secondary=association, back_populates="child", uselist=True, lazy="selectin", cascade="delete")

                def one_table():  # noqa
                    """ Тут описана связь многие-ко-многим из одной таблицы в саму себя. Это нужно например для реализации
                    подписчиков (юзер может подписаться на юзера и наоборот). """
                    association = Table(  # noqa
                        "associations",
                        Base.metadata,  # noqa
                        Column("following", Integer, ForeignKey("users.id"), primary_key=True),  # noqa
                        Column("follower", Integer, ForeignKey("users.id"), primary_key=True),  # noqa
                    )

                    class User(Base):  # noqa
                        __tablename__ = "users"  # noqa
                        name: Mapped[str]
                        following: Mapped[List["User"]] = relationship(
                            "User", cascade="delete", lazy="immediate", uselist=True, secondary="associations", back_populates="follower",
                            primaryjoin="User.id == associations.c.following", secondaryjoin="User.id == associations.c.follower",
                        )
                        follower: Mapped[List["User"]] = relationship(
                            "User", cascade="delete", lazy="immediate", uselist=True, secondary="associations", back_populates="following",
                            primaryjoin="User.id == associations.c.follower", secondaryjoin="User.id == associations.c.following",
                        )

        async def start():  # Создание таблиц в асинхронном виде. Base.metadata.create_all() - для синхронного создания таблиц.
            async with async_engine.begin() as conn:  # noqa
                await conn.run_sync(Base.metadata.create_all)  # Base.metadata.drop_all() - для удаления таблиц.

        async def end():  # noqa
            await session.close()  # Закрывает асинхронную сессию # noqa
            await engine.dispose()  # Закрывает асинхронное соединение # noqa

        asyncio.run(start())


class Peewee:
    """ Тут расписана работа с SQL базой данных на ORM Peewee. """
    @staticmethod
    def pattern():
        import functools  # noqa
        from typing import Callable, Optional  # noqa
        import peewee  # pip install peewee # noqa

        db = peewee.SqliteDatabase('/database.sql')

        class BaseModel(peewee.Model):
            """Базовый класс связывающий дочерние классы с файлом датабазы"""  # noqa

            class Meta:
                database = db

        class User(BaseModel):
            """Класс пользователя, регистрирует пользователя"""
            user_id = peewee.IntegerField(primary_key=True)
            username = peewee.CharField()
            first_name = peewee.CharField()
            last_name = peewee.CharField(null=True)

        db.create_tables([User])

        User.create(user_id='user_id', username='username', first_name='first_name', last_name='last_name').save()
        User.get(user_id='user_id')
