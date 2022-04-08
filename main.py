from scrapy.crawler import CrawlerProcess
from tutorial.tutorial.spiders.generate_prospect_by_company_size_using_btn import ProspectSpiderPerCompanySize

# run spider
process = CrawlerProcess(settings={
    'FEED_URI' : 'name_company_link_company_size.csv',
    'FEED_FORMAT' : 'csv'
})
process.crawl(ProspectSpiderPerCompanySize)
process.start()
