import sys

import requests
import scrapy
from ..items import CarsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging


class CarSpider(scrapy.Spider):
    name = 'cars'
    start_urls = [
        # 'https://quotes.toscrape.com'
        # 'https://www.polovniautomobili.com/auto-oglasi/pretraga',
        'https://www.mojauto.rs/rezultat/status/automobili/vozilo_je/polovan/poredjaj-po/oglas_najnoviji/po_stranici/60/prikazi_kao/lista/',
        # 'https://www.mojtrg.rs/'
    ]

    def __init__(self):
        super(CarSpider, self).__init__()
        self.mLogger = logging.getLogger('data.collecting')

    def parse(self, response, **kwargs):
        containers = response.css("div.resultWrap div.panelList")
        link = containers[0].css("a.addImg ::attr(href)").get()
        yield response.follow(link, callback=self.parseItem)

        for div in containers:
            link = div.css("a.addImg ::attr(href)").get()
            if link is not None:
                yield response.follow(link, callback=self.parseItem)
            else:
                self.mLogger.error('ERROR link is null')

        next_page = response.css("div.pagination").xpath("//a[@class='pag_next']").xpath("@href")[0].get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parseItem(self, response, **keywords):
        if response is None:
            self.mLogger.error('Response is None!')

        item = CarsItem()

        # TODO Fix error list index out of range

        # Init with dumb data
        item['prosecna_potrosnja'] = '0'
        item['ubrzanje'] = '0'
        item['prtljaznik'] = '0'

        item['broj_brzina'] = '0'
        item['pozicija_volana'] = 'Leva'
        item['pogon'] = None
        item['boja_unutrasnjosti'] = None
        item['klima'] = None
        item['broj_sedista'] = '0'
        item['broj_vrata'] = '0'

        item['naziv'] = response.css("div.singleOverview h1::text")[0].extract()
        item['cena'] = response.css(".sidebarPrice").css("span.priceReal::text")[0].extract()

        temp_div = response.css(".basicSingleData")
        item['godiste'] = temp_div[0].css("li")[1].css("span::text").extract_first()
        item['gorivo'] = temp_div[0].css("li")[3].css("span::text")[1].get()

        tech_divs = response.css("ul.techSpec")

        lis1 = tech_divs[0].css("li")
        for index, li in enumerate(lis1):
            att_tag = li.css("span::text").get()
            value = li.css("strong::text").get()

            attributes = {
                'Kubikaža': 'kubikaza',
                'Snaga': 'snaga',
                'Prešao kilometara': 'kilometraza',
                'Tip motora': 'tip_motora',
                'Pogon': 'pogon',
                'Menjač': 'tip_menjaca',
                'Broj brzina': 'broj_brzina',
                'Broj vrata': 'broj_vrata',
                'Broj sedišta': 'broj_sedista',
                'Strana volana': 'pozicija_volana',
                'Klima': 'klima',
                'Boja': 'boja',
                'Boja unutrašnjosti': 'boja_unutrasnjosti',
                'Kategorija': 'kategorija_vozila'
            }

            att = attributes.get(att_tag, "none")
            if att != "none":
                item[att] = value

        lis2 = tech_divs[1].css("li")
        for index, li in enumerate(lis2):
            att_tag = li.css("span::text").get()
            value = li.css("strong::text").get()

            attributes = {
                'Havarisano': 'havarisano',
                'Garažiran': 'garaziran',
                'Vozilo je': 'nov',
                'Servisna knjižica': 'servisna_knjizica',
                'Registrovano do': 'registrovano'
            }

            att = attributes.get(att_tag, "none")
            if att != "none":
                item[att] = value

        self.mLogger.debug(response.request.url)

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
