import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from logzero import logger
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
url = 'https://www.securite-routiere.gouv.fr/employeurs-engages/liste-des-employeurs-engages-page-1-57?page=1&range=All&zipcode=All&date%5Bmin%5D=2018-01-01&date%5Bmax%5D=2018-12-31&date%5Btype%5D=date&date%5Bvalue%5D='

driver.get(url)
driver.implicitly_wait(10)
# Explicit wait
wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-item")))

next = driver.find_elements(By.CLASS_NAME, 'page-item')

check_if_disabled = driver.find_element(By.CLASS_NAME, "page-item.disabled")

coockie_acept_btn = driver.find_element(By.XPATH, '//*[@id="footer_tc_privacy_button_3"]')

coockie_acept_btn.click()

current_url = driver.current_url


next[-2].click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-item")))


if current_url == driver.current_url:
    print("c'est la meme page")
else:
    print("ce n'est pas la meme page")

time.sleep(5)

