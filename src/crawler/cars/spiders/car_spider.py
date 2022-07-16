import requests
import scrapy
from ..items import CarsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        # 'https://quotes.toscrape.com'
        # 'https://www.polovniautomobili.com/auto-oglasi/pretraga',
        'https://www.mojauto.rs/rezultat/status/automobili/vozilo_je/polovan/poredjaj-po/oglas_najnoviji/po_stranici/60/prikazi_kao/lista/',
        # 'https://www.mojtrg.rs/'
    ]

    def parse(self, response, **kwargs):
        containers = response.css("div.resultWrap div.panelList")

        for div in containers:
            link = div.css("a.addImg ::attr(href)").get()
            if link is not None:
                yield response.follow(link, callback=self.parseItem)
            else:
                print('ERROR link is null')

        # bttn = response.xpath("//a[@title='Sledeća stranica']").xpath("@href")[0].get()
        # print(bttn)

        # if m_bttn.css("::text")[0].extract().strip() == "Следеће":
        #     next_page = m_bttn.xpath("@href")[0].extract()
        #     print(next_page)
        #     yield response.follow(next_page, callback=self.parse)

    def parseItem(self, response, **keywords):
        if response is None:
            print('ERROR')

        item = CarsItem()
        item['name'] = response.css("div.singleOverview h1::text")[0].extract()
        item['price'] = response.css(".sidebarPrice").css("span.priceReal::text")[0].extract()

        info_divs = response.css("singleBoxPanel")

        # item['production_year'] = container.xpath("//a[@title='Преузимање']").xpath("@href")[0].extract()
        item['production_year'] = response.css(".basicSingleData")[0].css("li")[1].css("span::text").extract_first()

        yield item

# XPATH scraping
#   response.xpath("//title/text()").extract()
#   response.xpath("//span[@class='text']/text()").extract()
#   response.xpath("@href").extract()    -   Returns param inside tag.
#   response.xpath("@href").extract_first()  - Returns first match
