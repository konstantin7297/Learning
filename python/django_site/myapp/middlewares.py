from django.http import HttpRequest


def set_useragent_on_request_middleware(get_response):  # Создается при запуске приложения. get_response - Получение запросов. Типа декоратор. # noqa
    """ Настройка логики между созданием запроса и получением ответа. Middleware нужно подключить в 'settings.py'. """
    def middleware(request: HttpRequest):  # Тут делается сам запрос, можно настроить: 'before' и 'after' request.
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)  # Делается сам запрос.
        return response  # Возвращается результат работы запроса.
    return middleware  # Возвращается сам запрос, уже измененный как надо.


class CountRequestsMiddleware:  # Класс, который считает, сколько запросов, ответов, ошибок получил сервер.
    """ Настройка мониторинга количества запросов, ответов и ошибок. Middleware нужно подключить в 'settings.py'. """
    def __init__(self, get_response):  # Создается при запуске приложения.
        self.get_response = get_response  # Получение запросов. Типа декоратор.
        self.requests_count = 0  # Количество запросов.
        self.responses_count = 0  # Количество ответов.
        self.exceptions_count = 0  # Количество ошибок.

    def __call__(self, request: HttpRequest):  # Запускается при вызове.
        self.requests_count += 1  # Добавляется 1 запрос.
        response = self.get_response(request)  # Выполняется запрос и получает результат его работы.
        self.responses_count += 1  # Добавляется 1 ответ.
        return response  # Отправляется выполненный запрос.

    def process_exception(self, request: HttpRequest, exception: Exception):  # noqa
        self.exceptions_count += 1  # Добавляет 1 ошибку. Тут же можно вернуть запрос, обработать его дополнительно и посмотреть ошибку.
