"""
Command to generate CSV : scrapy crawl generalprospectbybtn -o name_company_link.csv
"""

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logger
from webdriver_manager.chrome import ChromeDriverManager


class ProspectItem(scrapy.Item):
    company_name = scrapy.Field()
    name_signatory = scrapy.Field()
    link_company = scrapy.Field()


class ProspectSpiderLinkUsingNextBtn(scrapy.Spider):
    name = "generalprospectbybtn"
    allowed_domains = ["toscrape.com"]
    custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8',
                       'FEED_URI': 'CSV/name_company_link.csv'}

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_prospect)

    def parse_prospect(self, response):
        page_count = 1
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = 'https://www.securite-routiere.gouv.fr/employeurs-engages/liste-des-employeurs-engages-page-1-57?page=1&range=All&zipcode=All'
        driver.get(url)
        driver.implicitly_wait(10)
        # Explicit wait
        wait = WebDriverWait(driver, 5)

        # Accept Cookie (necessary or impossble to click on next btn)
        coockie_accept_btn = driver.find_element(By.XPATH, '//*[@id="footer_tc_privacy_button_3"]')
        coockie_accept_btn.click()

        for i in range(0, 200):

            driver.implicitly_wait(10)
            # Explicit wait
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "company-item")))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-item")))
            next_btn = driver.find_elements(By.CLASS_NAME, 'page-item')


            # Go to scrapy
            sel = scrapy.Selector(text=driver.page_source)

            # Find company name
            companies = sel.css("li.company-item")

            for company in companies:
                company_name = company.css("p::text").get()
                name_signatory = company.css("p.signatory::text").get()
                link_company = company.css("div.img-wrapper a.link-over ::attr(href)").extract()

                item = ProspectItem()
                item["company_name"] = company_name
                item["name_signatory"] = name_signatory
                item["link_company"] = link_company

                yield item

            logger.info(f"Scraping page :{page_count}")
            page_count += 1

            # Terminating and reinstantiating webdriver every 200 URL to reduce the load on RAM
            if (i != 0) and (i % 200 == 0):
                driver.quit()
                logger.info("Chromedriver restarted")

            next_btn[-2].click()  # Click on next btn

        logger.info(f"Scraped {page_count} PM2.5 readings.")
        driver.quit()
