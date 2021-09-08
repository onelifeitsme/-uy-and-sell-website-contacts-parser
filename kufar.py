from selenium import webdriver
from time import sleep
import csv


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*', 'x-client-data': 'VGo9iQEIorbJAQjEtskBCKmdygEI9tDKAQiMnssBCKKgywEI3PLLAQjv8ssBCM72ywEIs/jLAQie+csBCPv5ywEIvv8KBU=='}

print("Введите запрос для парсинга на Куфаре")
product = input()
product = str(product)

driver = webdriver.Chrome()

driver.get(f'https://www.kufar.by/listings?ot=1&query={product}')
sleep(1)
if driver.find_element_by_xpath('//*[@id="portal"]/div/div[2]/div[1]/div'):
    driver.find_element_by_xpath('//*[@id="portal"]/div/div[2]/div[1]/div/div[3]/div/img').click()
sleep(2)

driver.find_element_by_xpath('//*[@id="header"]/div[2]/div[3]/div/div/button').click()
user_name = driver.find_element_by_id("email")
user_name.send_keys("forever21yong@gmail.com")
password = driver.find_element_by_id("password")
password.send_keys("ForeverYoung23")
driver.find_element_by_xpath('//*[@id="__next"]/div[4]/div/form/div[4]/button').click()
sleep(2)
# # if driver.find_element_by_css_selector('') добавить потом избавление от уведомлений
base = []
items = []
try:
    pages_number = driver.find_element_by_xpath('//*[@id="main-content"]/div[4]/div[1]/div[2]/div[2]/div[3]/div/div/a[3]').text
    pages_number = int(pages_number)
except:
    pages_number = 1



def get_items_on_page(items):
    count = 0
    links = []
    sleep(2)
    urls = driver.find_elements_by_tag_name('a')
    for url in urls:
        links.append(url.get_attribute('href'))
    for link in links:
        if "item" in link or "kufar.by/vi/" in link:
            count +=1
        if count > 3:
            items.append(link)



def new_page(next_page, pages_number):
    for i in range(pages_number):
        get_items_on_page(items)
        gogogo = f'//a[contains(text(),"{next_page}")]'

        sleep(3)
        driver.execute_script("window.scrollTo(0, 7000)")
        sleep(3)
        try:
            a = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, gogogo)))
            a.click()
        except:pass
        next_page += 1



def data_parse(ad_item):
    driver.get(ad_item)
    try:
        driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[3]/div/div[1]/div[2]/div[3]/div/div/div/div[1]/div[2]/div[2]/button[1]').click()
    except:
        driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[3]/div/div[3]/div/div/div[1]/div[2]/div[2]/button[1]').click()

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


next_page = 2
gogogo = f'//a[contains(text(),"{next_page}")]'



new_page(next_page, pages_number)
sleep(2)



ad_item = 0
for i in range(len(items)):
    data_parse(items[ad_item])
    ad_item +=1


print(base)
for i in items:
    print(i)


with open("zhaba.csv", "a") as temp:
    polya = ['name', 'phone']
    out = csv.DictWriter(temp, fieldnames=polya)
    out.writeheader()
    for i in base:
        out.writerow(i)
for i in base:
    print(i)