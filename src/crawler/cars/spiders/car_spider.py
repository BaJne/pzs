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

        next_page = response.css("div.pagination").xpath("//a[@class='pag_next']").xpath("@href")[0].get()
        print(next_page)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseItem(self, response, **keywords):
        if response is None:
            print('ERROR')

        item = CarsItem()
        item['naziv'] = response.css("div.singleOverview h1::text")[0].extract()
        item['cena'] = response.css(".sidebarPrice").css("span.priceReal::text")[0].extract()

        temp_div = response.css(".basicSingleData")
        item['godiste'] = temp_div[0].css("li")[1].css("span::text").extract_first()
        item['gorivo'] = temp_div[0].css("li")[3].css("span::text")[1].get()

        tech_divs = response.css("ul.techSpec")

        lis1 = tech_divs[0].css("li")
        for index, li in enumerate(lis1):
            value = li.css("strong::text").get()

            attributes = {
                0: 'kubikaza',
                1: 'snaga',
                2: 'kilometraza',
                4: 'tip_motora',
                5: 'pogon',
                6: 'tip_menjaca',
                7: 'broj_brzina',
                8: 'broj_vrata',
                9: 'broj_sedista',
                10: 'pozicija_volana',
                11: 'klima',
                12: 'boja',
                13: 'boja_unutrasnjosti',
                14: 'kategorija_vozila'
            }

            att = attributes.get(index, "none")
            if att != "none":
                item[att] = value

        for m in response.css("iframe"):
            rating_div = m.xpath("@src").get()
            yield response.follow(rating_div, callback=self.get_rating, cb_kwargs=item)

    def get_rating(self, response, **keywords):
        ratings = response.css("div.car-preview-rating-value::text")

        if len(ratings) < 3:
            yield keywords
            return

        keywords['prosecna_potrosnja'] = ratings[0].get().strip()
        keywords['ubrzanje'] = ratings[2].get().strip()
        keywords['prtljaznik'] = ratings[4].get().strip()

        yield keywords


# XPATH scraping
#   response.xpath("//title/text()").extract()
#   response.xpath("//span[@class='text']/text()").extract()
#   response.xpath("@href").extract()    -   Returns param inside tag.
#   response.xpath("@href").extract_first()  - Returns first match
