from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

from pymongo import MongoClient
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.get('https://m.mail.ru/login')

assert "Вход — Почта Mail.Ru" in driver.title



#elem = WebDriverWait(driver, 10).until(
#    EC.presence_of_element_located((By.NAME, 'Login'))
#)

time.sleep(1)
elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

elem = driver.find_elements_by_class_name('footer__row')
elem = elem[4].find_element_by_class_name('footer__link')
driver.get(elem.get_attribute('href'))

links = []
mail_letters = []
i = 0

for k in range(10):
    letters = WebDriverWait(driver,3).until(
            EC.presence_of_all_elements_located((By.XPATH,"//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']"))
        )
    #отдельно складываем ссылки в список
    for letter in letters:
        if letter.get_attribute('href') not in links:
            links.append(letter.get_attribute('href'))

    #работаем только с новой частью списка
    for link in links[i:len(links)]:
        base_dict = {}
        driver.get(link)
        name_elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='thread__subject thread__subject_pony-mode']"))
        )
        base_dict['name'] = name_elem.text
        date_elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='letter__date']"))
        )
        base_dict['date'] = date_elem.text

        contact_elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='letter-contact']"))
        )
        base_dict['contact'] = contact_elem.text
        print(base_dict)
        driver.back()
        mail_letters.append(base_dict)
        time.sleep(1)
        break

    i = len(links)
    #скролим
    elems = WebDriverWait(driver,3).until(
            EC.presence_of_all_elements_located((By.XPATH,"//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']"))
        )
    action = ActionChains(driver)
    action.move_to_element(elems[-1])
    action.perform()


client = MongoClient('localhost',27017)
db = client['LettersDB']
db_letters = db.letters

for let in mail_letters:
    if not db_letters.count_documents(let):
        db_letters.insert_one(let)




