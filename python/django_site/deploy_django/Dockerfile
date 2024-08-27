FROM python:3.10

ENV PYTHONUNBUFFERED=1  # Возвращает вывод в консоль логов от приложения в Docker-контейнере.

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.4.2"
RUN poetry config virtualenvs.create false --local  # Выключает создание виртуального окружения, т.к. контейнер уже им является.
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
