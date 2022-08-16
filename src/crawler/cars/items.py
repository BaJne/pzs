# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarsItem(scrapy.Item):
    # TEHNICKI PODACI
    naziv = scrapy.Field()
    cena = scrapy.Field()
    godiste = scrapy.Field()
    gorivo = scrapy.Field()

    kubikaza = scrapy.Field()               # cm3
    snaga = scrapy.Field()                  # KS (Konjskih snaga)
    kilometraza = scrapy.Field()            # km
    tip_motora = scrapy.Field()
    pogon = scrapy.Field()
    tip_menjaca = scrapy.Field()
    broj_brzina = scrapy.Field()            # broj
    broj_vrata = scrapy.Field()             # broj vrata
    broj_sedista = scrapy.Field()
    pozicija_volana = scrapy.Field()
    klima = scrapy.Field()
    boja = scrapy.Field()
    boja_unutrasnjosti = scrapy.Field()
    kategorija_vozila = scrapy.Field()

    prosecna_potrosnja = scrapy.Field()     # broj l|100km
    ubrzanje = scrapy.Field()
    prtljaznik = scrapy.Field()

    # Istorija vozila
    servisna_knjizica = scrapy.Field()
    registrovano = scrapy.Field()
    havarisano = scrapy.Field()
    garaziran = scrapy.Field()
    nov = scrapy.Field()
