import scrapy
from bs4 import BeautifulSoup

class OlxSpider(scrapy.Spider):
    name = 'olx'

    start_urls = [
        "https://www.olx.ua/elektronika/telefony-i-aksesuary/"
        ]

    def parse(self, response):
        html = BeautifulSoup(response.body, 'html')
        goods = html.find_all('tr', class_='wrap')
        for good in goods:
            url = good.find('a')
            yield scrapy.Request(url, self.parse_good)

    def parse_good(self, response):
        html = BeautifulSoup(response.body, 'html')
        title = html.find('div', class_='offer-titlebox').get_text()
        pub_date = html.find('em').get_text().split(',')
        description = html.find(id_='textContent')

