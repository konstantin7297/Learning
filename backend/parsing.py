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
    def selenium_parsing(url="https://v2.vost.pw/tip/tv/3103-youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-3rd-season.html"): # noqa
        """ Парсинг через Selenium: pip install selenium """
        from selenium import webdriver  # Сам браузер # noqa
        from selenium.webdriver.common.by import By  # Нужен для перемещения по элементам сайта # noqa
        from selenium.webdriver.chrome.options import Options  # Нужен для настройки самого окна браузера и его параметров # noqa
        from selenium.webdriver.remote.webelement import WebElement  # Для аннотаций # noqa
        from selenium.webdriver.support.wait import WebDriverWait # Нужен для ожидания загрузки элементов на странице # noqa
        from selenium.webdriver.support import expected_conditions as EC # Нужен для ожидания загрузки элементов на странице # noqa

        class Browser:
            def __init__(self):
                options = Options()  # Создает класс настроек для браузера
                options.add_argument("--headless")  # Позволяет открывать браузер в фоне
                options.add_argument("--no-sandbox")  # Обход безопасности системы, что бы скрипт не вылетал из-за прав. Нужно в Docker например(т.к. он работает от прав root'а).
                options.add_argument('--ignore-ssl-errors')  # Игнор ошибок с загрузкой сертификата.
                options.add_argument('--ignore-certificate-errors-spki-list')  # Игнор ошибок с загрузкой сертификата.
                options.add_argument("--disable-dev-shm-usage")  # Отключение использования /dev/shm/, его размер мал, из-за чего возникают ошибки.
                options.add_argument("--window-size=1600,900")  # разрешение экрана окна браузера | '--start-maximized' - полный экран  # noqa
                options.add_argument(f"user-data-dir=C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data")  # Windows data # noqa
                options.add_argument(f"user-data-dir=/home/{getpass.getuser()}/.config/google-chrome")  # Берет активную версию браузера(с ее авторизациями) в ubuntu data # noqa
                options.add_argument('profile-directory=Default')  # Эти 2 строки для Ubuntu авто-авторизации. Тут папка профиля браузера. chrome://version/ # noqa
                self.driver = webdriver.Chrome(options=options)  # Создает драйвер браузера Chrome с указанными настройками # noqa

        browser = Browser()
        browser.driver.get(url)  # открывает браузер с указанной ссылкой # noqa
        browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # прокрутит курсор вниз # noqa
        browser.driver.execute_script("arguments[0].scrollIntoView();", element)  # прокрутит курсор до какого то элемента # noqa
        browser.driver.execute_script("arguments[0].innerHTML = '{}'".format("text"), press_btn)  # ввести значение со смайлом в строку через javascript # noqa
        browser.driver.save_screenshot('screenshot.png')  # сделать скриншот
        html = browser.driver.page_source  # возвращает html код открытого сайта # noqa
        nav_tags = browser.driver.find_elements(by=By.TAG_NAME, value="nav")  # позволяет найти все теги nav в html коде # noqa
        print(nav_tags[0].text)  # Вывести информацию # noqa

        btns_obj = WebDriverWait(browser.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/div/div/div/button[3]'))
        )  # noqa
        ActionChains(browser.driver).move_to_element(btns_obj).perform()  # Ждет загрузки элемента, а потом наводит на него курсор. # noqa

        element = WebDriverWait(browser.driver, 15).until(EC.element_to_be_clickable((By.TAG_NAME, "nav")))  # ждет пока сайт загрузит нужные элементы # noqa
        element.get_attribute("innerHTML")  # Получает внутренности своего тега # noqa
        element.get_attribute("outerHTML")  # Получает внутренности тега-родителя # noqa
        element.send_keys()  # для отправки текста в это поле. # noqa
        element.click()  # для нажатия кнопки. # noqa
        browser.driver.quit()  # Закрывает драйвер # noqa

    @staticmethod
    def scrapy(url="https://v2.vost.pw/tip/tv/3103-youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e-3rd-season.html"): # noqa
        """ Парсинг на scrapy, особенности: быстрый, асинхронный полноценный инструмент для парсинга, огромный функционал, но сложный """ # noqa
        # pip install scrapy
