from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*', 'x-client-data': 'VGo9iQEIorbJAQjEtskBCKmdygEI9tDKAQiMnssBCKKgywEI3PLLAQjv8ssBCM72ywEIs/jLAQie+csBCPv5ywEIvv8KBU=='}

print("Введите запрос для парсинга на Куфаре")
product = input()
product = str(product)

driver = webdriver.Chrome()

# ЗАХОДИМ НА САЙТ С ЗАПРОСОМ В ПОИСКЕ, ВКЛЮЧАЮЩЕМ ВВЕДЁННЫЙ ТОВАР
driver.get(f'https://www.kufar.by/listings?ot=1&query={product}')
sleep(1)
# if driver.find_element_by_xpath('//*[@id="portal"]/div/div[2]/div[1]/div'):
#     driver.find_element_by_xpath('//*[@id="portal"]/div/div[2]/div[1]/div/div[3]/div/img').click()
# sleep(2)


# АВТОРИЗАЦИЯ
def login():
    driver.find_element(By.XPATH, '//button[text()="Войти"]').click()
    user_name = driver.find_element(By.XPATH, '//input[@name="email"]')
    user_name.send_keys("ВАШ ЛОГИН")
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    password.send_keys("ВАШ ПАРОЛЬ")
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    sleep(2)
# # if driver.find_element_by_css_selector('') добавить потом избавление от уведомлений


base = []
items = []

# ПОЛУЧТЕНИЕ КОЛИЧЕСТВА СТРАНИЦ ВЫДАЧИ
pages_number = driver.find_element(By.XPATH, '//div[@data-name="listings-pagination"]').text
pages_number = int(pages_number[-1])

# ПОЛУЧЕНИЕ ССЫЛОК НА ОБЪЯВЛЕНИЯ НА ОДНОЙ СТРАНИЦЕ.ИСКЛЮЧАЕМ ПЛАТНЫЕ ОБЪЯВЛЕНИЯ НЕ ПО ТЕМЕ
def get_items_on_page():
    all_ads = driver.find_elements(By.XPATH, '//article/a')
    minus = driver.find_elements(By.XPATH, '//div[@data-name="card-icon-polepos"]/ancestor::article/a')
    for ad in all_ads:
        if ad not in minus:
            items.append(ad.get_attribute('href'))






def next_page(i):
    page = driver.find_element(By.XPATH, f'//div[@data-name="listings-pagination"]/descendant::a[text()="{i}"]')
    page.click()
    sleep(4)


#
#
# ПРОХОД ВСЕХ СТРАНИЦ ВЫДАЧИ И ПОЛУЧЕНИЕ ССЫЛОК НА ОБЪЯВЛЕНИЯ
def get_ads_on_all_pages():
    for i in range(pages_number+1):
        if i > 1:
            next_page(i)
            get_items_on_page()
            print(len(items))


# sex = items[0]
# driver.get(sex)
# sleep(3)
# driver.find_element(By.XPATH, '//button[@data-name="call_button"]').click()
#
def data_parse():
    sleep(3)
    try:
        driver.find_element(By.XPATH, '//button[@data-name="call_button"]').click()
    except:
        pass
    sleep(3)
    try:
        phone = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-name="phone-number-modal"]/a'))).text
        name = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-name="phone-number-modal"]/div'))).text
        base.append({
            "name": name,
            "phone": phone,
        })
    except:
        pass


def writing_data_to_csv():
    with open("kufar.csv", "a") as temp:
        polya = ['name', 'phone']
        out = csv.DictWriter(temp, fieldnames=polya)
        out.writeheader()
        for i in base:
            out.writerow(i)


login()
# ПОЛУЧТЕНИЕ КОЛИЧЕСТВА СТРАНИЦ ВЫДАЧИ
pages_number = driver.find_element(By.XPATH, '//div[@data-name="listings-pagination"]').text
pages_number = int(pages_number[-1])
# ПОЛУЧЕНИЕ ССЫЛОК НА ОБЪЯВЛЕНИЯ НА ОДНОЙ СТРАНИЦЕ.ИСКЛЮЧАЕМ ПЛАТНЫЕ ОБЪЯВЛЕНИЯ НЕ ПО ТЕМЕ
get_items_on_page()
# ПРОХОД ВСЕХ СТРАНИЦ ВЫДАЧИ И ПОЛУЧЕНИЕ ССЫЛОК НА ОБЪЯВЛЕНИЯ
get_ads_on_all_pages()

for item in items:
    driver.get(item)
    sleep(4)
    data_parse()
    writing_data_to_csv()
    sleep(4)

