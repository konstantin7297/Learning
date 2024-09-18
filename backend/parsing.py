class Selenium:
    """ Парсинг через Selenium: pip install selenium """
    from getpass import getuser   # noqa
    from selenium import webdriver  # Сам браузер  # noqa
    from selenium.webdriver.common.by import By  # Нужен для перемещения по элементам сайта  # noqa
    from selenium.webdriver.chrome.options import Options  # Нужен для настройки самого окна браузера и его параметров  # noqa
    from selenium.webdriver.remote.webelement import WebElement  # Для аннотаций  # noqa
    from selenium.webdriver.support.wait import WebDriverWait  # Нужен для ожидания загрузки элементов на странице  # noqa
    from selenium.webdriver.support.select import Select  # Нужен для работы с выпадающими списками  # noqa
    from selenium.webdriver.support import expected_conditions as EC  # Нужен для ожидания загрузки элементов на странице  # noqa

    def __init__(self, main_url: str, timeout: int = 5):
        """ Базовая настройка selenium """  # setTimeout(function() { debugger; }, 5000);  - останавливает выполнение JS для поиска элементов. # noqa
        options = Options()  # Создает класс настроек для браузера.  # noqa
        options.add_argument("--start-maximized")  # разрешение экрана окна браузера | '--window-size=1600,900' - полный экран  # noqa
        options.add_argument('--ignore-ssl-errors')  # Игнор ошибок с загрузкой сертификата.
        options.add_argument('--ignore-certificate-errors-spki-list')  # Игнор ошибок с загрузкой сертификата.
        options.add_argument('--disable-cache')  # Выключает сохранение всяких картинок и прочих ресурсов в кэше. # noqa
        options.add_argument("--disable-dev-shm-usage")  # Отключение использования /dev/shm/, его размер мал, из-за чего возникают ошибки.
        options.add_argument("--no-sandbox")  # Обход безопасности системы, что бы скрипт не вылетал из-за прав. Нужно в Docker например(т.к. он работает от прав root'а).
        options.add_argument("--incognito")  # Позволяет открывать браузер в режиме инкогнито. # noqa
        options.add_argument("--proxy-server=IP")  # Устанавливаем proxy. Для аутентификации в proxy формат такой: 'username:password@ip:port'. # noqa
        options.add_argument("--headless")  # Позволяет открывать браузер в фоне. # noqa
        options.add_argument("--disable-blink-features=AutomationControlled")  # Говорит сайтам, что браузером управляет человек, а не бот. # noqa
        options.add_argument("--user-agent=...")  # Позволяет установить user-agent. Нужен к верхнему параметру, что сказать, что браузером управляет не бот. # noqa
        options.page_load_strategy = "eager"  # Стратегия загрузки, которая не ждет загрузки картинок и всего такого. Грузит только DOM. # noqa
        options.add_experimental_option("prefs", {"download.default_directory": f"{os.getcwd()}/uploads"})    # Папка для сохранения загруженных файлов. # noqa

        if sys.platform == "win32":  # Подключается к профилю пользователя в Windows. # noqa
            options.add_argument(f"user-data-dir=C:\\Users\\{getuser()}\\AppData\\Local\\Google\\Chrome\\User Data")  # Windows data # noqa
        else:  # Подключается к профилю пользователя НЕ в Windows. Пример для Linux больше. # noqa
            options.add_argument(f"user-data-dir=/home/{getuser()}/.config/google-chrome")  # Берет активную версию браузера(с ее авторизациями) в ubuntu data # noqa
            options.add_argument('profile-directory=Default')  # Эти 2 строки для Ubuntu авто-авторизации. Тут папка профиля браузера. chrome://version/ # noqa

        self.driver = webdriver.Chrome(options=options)  # Создает драйвер браузера Chrome с указанными настройками # noqa
        self.wait = WebDriverWait(self.driver, timeout).until  # Создает заготовку для ожидания загрузки будущих объектов. # noqa
        self.action = ActionChains(self.driver)  # Создает заготовку для каких то действий к будущим объектам. Например навести курсор. # noqa
        self.url = main_url

    def patterns(self):
        """ Примеры работы с selenium объектами """
        self.driver.get(self.url)  # открывает браузер с указанной ссылкой  # noqa
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # прокрутит курсор вниз  # noqa
        self.driver.execute_script("arguments[0].scrollIntoView();", element)  # прокрутит курсор до какого то элемента  # noqa
        self.driver.execute_script("arguments[0].innerHTML = '{}'".format("text"), press_btn)  # ввести значение со смайлом в строку через javascript  # noqa
        self.driver.save_screenshot('screenshot.png')  # сделать скриншот  # noqa
        self.driver.quit()  # Закрывает драйвер # noqa
        elem = self.driver.page_source  # возвращает html код открытого сайта # noqa
        elem = self.driver.find_element(By.XPATH, "//input[@type='file']")  # Пример удобного нахождения элементов по 'xpath'. Еще: //button[text()='Remove'] # noqa
        elem = self.driver.find_elements(by=By.TAG_NAME, value="nav")  # позволяет найти все теги nav в html коде. Отдает объекты, с которыми можно работать # noqa
        elem = self.wait(EC.element_to_be_clickable((By.ID, "tag_id")))  # Ожидает конкретное поведение объекта и после возвращает его # noqa
        elem = self.action.move_to_element(elem).perform()  # Ждет загрузки элемента, а потом наводит на него курсор. # noqa
        elem = Select(self.driver.find_element("xpath", "//select[@id='dropdown']"))  # Получаем объект выпадающего списка для выбора параметра. # noqa
        elem.get_attribute("innerHTML")  # Получает внутренности своего тега # noqa
        elem.get_attribute("outerHTML")  # Получает внутренности тега-родителя # noqa
        elem.send_keys(Keys.CTRL + "A")  # для отправки текста в это поле. # noqa
        elem.click()  # для нажатия кнопки. # noqa


class Parsing:
    """ Тут информация о парсинге данных. """  # noqa
    @staticmethod
    def api_parsing(): # noqa
        """ Грамотный парсинг по API. Сбор данных для запроса: сайт -> f12 -> network -> catalog... -> проверить preview та ли инфа -> catalog: copy as cURL bash """  # noqa
        import requests  # pip install requests # noqa

        """ Ссылка на сам сайт для парсинга, берется из cURL запроса """ # noqa
        url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json"  # noqa

        """ Прокси нужен, что бы не забанили по API """ # noqa
        proxies = {'http': 'http://da7f8169-414243:4isl336w9zw@185.132.177.55:41793'}

        """ Header берется из copy as cURL и переписывается в словарь """
        headers = {
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Referer': 'https://www.wildberries.ru/',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', # noqa
            'sec-ch-ua-platform': "Windows",
        }

        response = requests.get(url=url, headers=headers, proxies=proxies)  # noqa
        if response.status_code == 200:
            result = response.json()
            item = result[0].get("childs", {})[0].get("name", None)  # сбор инфы уже в классическом словаре # noqa

    @staticmethod
    def beautifulsoup4_parsing(url="https://v2.vost.pw/tip/tv/3103-youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-3rd-season.html"): # noqa
        """ Парсинг через BeautifulSoup4 """
        import requests  # pip install requests, bs4, lxml # noqa
        from bs4 import BeautifulSoup as bs  # noqa

        def authorization(): # noqa
            """ Парсинг html разметки вместе с авторизацией (DEEP-WEB контент - контент, где требуется авторизация) """
            # Проверяем через инструменты разработчика, как проходит процесс авторизации (ищем например /login запрос) Если там есть CSRF токен, его искать в html # noqa
            # Тут достаем CSRF ключ из html сайта
            session = requests.session()
            auth_html = session.get(url)  # noqa
            auth_bs = bs(auth_html.content, 'html.parser')
            csrf = auth_bs.select('input[name=YII_CSRF_TOKEN]')[0]['value']

            payload = {'YII_CSRF_TOKEN': csrf, 'login': 'mail@inbox.ru', 'password': '12345678'} # Проходим авторизацию: собераем указанные header, payload и т.д... # noqa
            answer = session.post('https://smartprogress.do/user/login/', data=payload) # делаем требуемый запрос с требуемыми параметрами авторизации # noqa
            html_item2 = bs(answer.content, 'lxml') # скармливаем контент в анализатор html # noqa

        response = requests.get(url)  # Делается гет запрос на сайт, stream=True - позволяет скачивать файлы постепенно (например 20гб) # noqa
        if response.status_code == 200:  # Проверяется, вернулась ли нужная инфа, lxml - быстрее, чем html.parser # noqa
            html_item = bs(response.text,'html.parser')  # Разбивает весь вернувшийся код на html теги. .text - декодированный вариант, .content - со значениями в битах # noqa

            for element in html_item.select('.container'):  # идет по всем элементам, на которых указан класс .container # noqa
                url = element.select('.btn > a')  # забирает все ссылки из кнопок с классом .btn  # noqa
                element1 = element.find_all(class_='name') # ищет по названию классов # noqa
                print(url[0].text)

    @staticmethod
    def scrapy(url="https://v2.vost.pw/tip/tv/3103-youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-3rd-season.html"): # noqa
        """ Парсинг на scrapy, особенности: быстрый, асинхронный полноценный инструмент для парсинга, огромный функционал, но сложный """ # noqa
        # pip install scrapy
