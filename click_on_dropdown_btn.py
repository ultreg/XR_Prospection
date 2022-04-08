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
url = 'https://www.securite-routiere.gouv.fr/employeurs-engages/liste-des-employeurs-engages-page-1-57?page=1&date%5Bmin%5D=2016-01-01&date%5Bmax%5D=2022-12-31&date%5Btype%5D=date&range=All&zipcode=All'

driver.get(url)
driver.implicitly_wait(10)
# Explicit wait
wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "filter-select.filter-select_date")))

drop_down_menu = driver.find_element(By.CLASS_NAME, "filter-select.filter-select_date")
drop_down_menu.click()

# Sleep neccessary to get text
time.sleep(1)

dropdown_menu_clicked = driver.find_element(By.CLASS_NAME, "dropdown-menu")
all_date_signator = dropdown_menu_clicked.text.strip().split("\n")

print("all :")
print(all_date_signator)

item = dropdown_menu_clicked.find_element(By.PARTIAL_LINK_TEXT, "2019")
item.click()

filtre_btn = driver.find_element(By.CLASS_NAME, "full.grey.cta-round")
filtre_btn.click()

time.sleep(5)