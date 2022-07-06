import scrapy


class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        # 'https://quotes.toscrape.com'
        'https://www.polovniautomobili.com/auto-oglasi/pretraga',
        # 'https://www.mojauto.rs/',
        # 'https://www.mojtrg.rs/'
    ]

    def parse(self, response, **kwargs):
        title = response.css('html').css('head').css('title::text').extract()
        print(title)
        yield {'titletext': title}

