from rest_framework.test import APIClient, RequestsClient, APIRequestFactory  # noqa
from django.contrib.auth.models import User  # noqa
from django.test import TestCase  # noqa
from django.urls import reverse  # noqa

from .models import Product


class GetCookieSessionTestCase(TestCase):  # Класс тестирует функцию получения 'cookie' и 'session' с помощью HTTP запросов. Название класса в формате: 'BlaTestCase'.
    """ Класс показывает пример, как можно протестировать HTTP запросы. Важно соблюдать названия классов и функций. По сути это unittests. Запуск: 'python manage.py myapp.tests.GetCookieSessionTestCase'. """  # noqa
    def test_get_cookie_session(self):  # Проверяем функции получения 'cookie' и 'session'. Название функции в формате: 'test_bla'.
        response = self.client.get(reverse("myapp:cookie_session_end"))  # Делает get запрос к URL.
        self.assertContains(response, "default")  # Проверяет, что в ответе есть указанный отрезок и успешный статус-код.


class ProductCreateViewTestCase(TestCase):
    """ Класс показывает пример, как можно протестировать класс CreateView. """
    def setUp(self) -> None:  # Функция поднастройки перед каждым тестом. setUpClass - в начале всех тестов в этом классе. # noqa
        self.product = "product1"  # Имя продукта для теста.
        Product.objects.filter(name=self.product).delete()  # Удаление продукта, если он уже есть в тестовой БД. # noqa

    def test_create_product(self):
        response = self.client.post(  # Делается POST запрос для создания продукта.
            reverse("myapp:ProductCreateView"),  # Адрес запроса.
            {"name": self.product, "price": "1500", "description": "description1", "discount": "15"},  # Тело запроса.
        )
        self.assertRedirects(response, reverse("myapp:ProductListView"))  # Проверяется, что после запроса было перенаправление на список продуктов и статус-код - перенаправление.
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())  # Проверяет, что новый продукт есть в тестовой БД. # noqa


class ProductDetailViewTestCase(TestCase):
    """ Класс показывает пример, как можно протестировать класс DetailView. """
    def setUp(self) -> None:  # Функция поднастройки перед каждым тестом. setUpClass - в начале всех тестов в этом классе. # noqa
        self.product = Product.objects.create(name="product2")  # Создаем продукт для теста. # noqa

    def tearDown(self) -> None:  # Функция выполняется после каждого теста. tearDownClass - после всех тестов в этом классе. # noqa
        self.product.delete()  # Удаляем созданный для теста продукт.

    def test_get_product(self):  # Проверяем продукт.
        response = self.client.get(reverse("myapp:ProductDetailView", kwargs={"pk": self.product.pk}))  # Делаем запрос.
        self.assertEqual(response.status_code, 200)  # Проверяем статус-код запроса.

    def test_get_product_and_check_content(self):  # Проверяем продукт.
        response = self.client.get(reverse("myapp:ProductDetailView", kwargs={"pk": self.product.pk}))  # Делаем запрос.
        self.assertContains(response, self.product.name)  # Проверяем, что на странице есть имя продукта и мы получили успешный статус-код.


class ProductListViewTestCase(TestCase):
    """ Класс показывает пример, как пользоваться fixture. Перед тестами Django будет заполнять тестовую БД этими данными, а после тестов удалять.  """
    fixtures = ["product.json"]  # fixture из папки fixtures.

    @classmethod
    def setUpClass(cls):  # Функция выполняется в начале всех тестов в этом классе. # noqa
        cls.user_info = dict(username="username", password="password")
        cls.user_obj = User.objects.create_user(**cls.user_info)  # noqa

    @classmethod
    def tearDownClass(cls):  # Функция выполняет после всех тестов в этом классе.
        cls.user_obj.delete()  # noqa

    def setUp(self):  # Функция выполняется перед каждым тестом.
        self.client.login(**self.user_info)  # Аутентификация пользователя для тестов. Первый вариант. # noqa
        self.client.force_login(self.user_obj)  # Принудительная аутентификация пользователя. Второй вариант. # noqa

    def test_products1(self):  # Первый вариант проверки, что список продуктов доступен на странице.
        response = self.client.get(reverse("myapp:ProductListView"))  # Запрашиваем страницу списка продуктов.
        for product in Product.objects.filter(archived=False).all():  # Пробегаемся по всем продуктам. # noqa
            self.assertContains(response, product.name)  # Проверяем, что на странице есть имена всех продуктов.

    def test_products2(self):  # Второй вариант проверки, что список продуктов доступен на странице.
        response = self.client.get(reverse("myapp:ProductListView"))  # Запрашиваем страницу списка продуктов.

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),  # Запрашиваем список продуктов. # noqa
            values=(product.pk for product in response.context["products"]),  # Берем список первичных ключей продуктов из context переменной.
            transform=lambda p: p.pk,  # Указывает, что брать из qs: функция принимает p - продукт, отдает его pk.
        )
        self.assertTemplateUsed(response, "myapp/2-rule.html")  # Проверяет, что в тесте был использован именно этот шаблон.


class RestFrameworkTestCase(TestCase):
    """ Класс для тестирования REST Framework API. Он тестируется несколько иначе. Подробности на WIKI. """
    def setUp(self):
        self.factory = RequestsClient()  # Через него тестируется API от REST Framework.

    def test_rest_framework_view(self):  # Тестирование функции 'rest_framework_view'.
        """ Это лишь маленький пример, там достаточно много параметров, включая необходимость смены типа данных, сериализаций и т.д. Смотреть WIKI. """  # noqa
        response = self.factory.get('http://localhost/api/products/')
        self.assertEqual(response.status_code, 200)
