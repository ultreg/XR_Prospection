from scrapy.crawler import CrawlerProcess
from generate_prospect_by_company_size_using_btn import ProspectSpiderPerCompanySize
from generate_prospect_by_county_using_btn import ProspectSpiderPerCountry
from generate_prospect_by_sign_date_using_btn import ProspectSpiderPerDate
from generate_prospect_company_name_link_using_next_btn import ProspectSpiderLinkUsingNextBtn
from manipulation_csv import manipulation_csv
import os


def checking_prospect_number():
    list_of_csv = os.listdir("Final CSV")
    if list_of_csv:
        for letter in list_of_csv[-1]:
            if letter.isnumeric():
                return int(letter) + 1
    else:
        print("No CSV file")
        return 1


num_of_prospect_file = checking_prospect_number()


class ScrappListEmployeEngage:
    def __init__(self):
        # run spider
        process = CrawlerProcess(settings={
            'FEED_FORMAT': 'csv'
        })
        process.crawl(ProspectSpiderPerCompanySize)
        process.crawl(ProspectSpiderPerCountry)
        process.crawl(ProspectSpiderPerDate)
        process.crawl(ProspectSpiderLinkUsingNextBtn)
        process.start()

        # Merge all csv in one
        manipulation_csv(num_of_prospect_file)

