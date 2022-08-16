# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import logging
from datetime import date

current_year = date.today().year


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


class CarsPipeline:

    def __init__(self):
        self.mLogger = logging.getLogger('data.collecting')
        self.create_connection()
        self.create_table()
        self.error_process = 0

    def create_connection(self):
        self.conn = sqlite3.connect(r"./../output/cars.db")
        self.curr = self.conn.cursor()

        # """
        #     CREATE TABLE car(
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         naziv text NOT NULL,
        #         cena number,
        #         godiste number,
        #         gorivo text,
        #         kubikaza number NULL,
        #         snaga number NULL,
        #         kilometraza number NULL,
        #         tip_motora text NULL,
        #         pogon text NULL,
        #         tip_menjaca text NULL,
        #         broj_brzina number NULL,
        #         broj_vrata number NULL,
        #         broj_sedista number NULL,
        #         pozicija_volana number NULL,
        #         klima number NULL,
        #         boja text NULL,
        #         boja_unutrasnjosti text NULL,
        #         kategorija_vozila text NULL,
        #         prosecna_potrosnja real NULL,
        #         ubrzanje real NULL,
        #         prtljaznik real NULL,
        #         servisna_knjizica number NULL,
        #         havarisano number NULL,
        #         garaziran number NULL,
        #         nov number NULL
        #     )
        # """

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS car""")
        self.curr.execute("""
            CREATE TABLE car(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naziv text NOT NULL,
                cena INTEGER,
                godiste INTEGER,
                gorivo text,
                kubikaza INTEGER NULL,
                snaga INTEGER NULL,
                kilometraza INTEGER NULL,
                tip_motora text NULL,
                pogon text NULL,
                tip_menjaca text NULL,
                broj_brzina INTEGER NULL,
                broj_vrata text NULL,
                broj_sedista INTEGER NULL,
                pozicija_volana text NULL,
                klima text NULL,
                boja text NULL,
                boja_unutrasnjosti text NULL,
                kategorija_vozila text NULL,
                prosecna_potrosnja text NULL,
                ubrzanje text NULL,
                prtljaznik text NULL,
                servisna_knjizica INTEGER DEFAULT 0,
                havarisano INTEGER DEFAULT 0,
                garaziran INTEGER DEFAULT 0,
                nov INTEGER DEFAULT 0,
                registrovano INTEGER DEFAULT 0
            ) 
        """)
        self.curr.execute("""DROP TABLE IF EXISTS car_temp""")
        self.curr.execute("""
            CREATE TABLE car_temp(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naziv text NOT NULL,
                cena text,
                godiste text,
                gorivo text,
                kubikaza text NULL,
                snaga text NULL,
                kilometraza text NULL,
                tip_motora text NULL,
                pogon text NULL,
                tip_menjaca text NULL,
                broj_brzina text NULL,
                broj_vrata text NULL,
                broj_sedista text NULL,
                pozicija_volana text NULL,
                klima text NULL,
                boja text NULL,
                boja_unutrasnjosti text NULL,
                kategorija_vozila text NULL,
                prosecna_potrosnja text NULL,
                ubrzanje text NULL,
                prtljaznik text NULL,
                servisna_knjizica text NULL,
                havarisano text NULL,
                garaziran text NULL,
                nov text NULL,
                registrovano text NULL
            ) 
        """)

    def to_number(self, value):
        if value.isnumeric():
            return int(value)
        else:
            try:
                return float(value)
            except ValueError:
                self.error_process = 1
                self.mLogger.error('Number conversion is not valid')
                return value

    def attribute_as_num(self, item):
        temp = self.to_number(item.split()[0])
        return temp

    def process_price(self, item):
        cena = item['cena']
        cena = remove_suffix(cena, "EUR")
        cena = cena.replace('.', '')
        cena = cena.strip()
        if cena.isnumeric():
            cena = int(cena)
        else:
            cena = item['cena']
            self.error_process = 1
            self.mLogger.error("Price is not valid.")
        return cena

    def process_age(self, item):
        temp = item['godiste'][0:4]
        if temp.isnumeric():
            godiste = int(temp)
            godiste = current_year - godiste
        else:
            godiste = temp
            self.error_process = 1
            self.mLogger.error("Age is not valid.")
        return godiste

    def is_attribute_present(self, item, att):
        if att in item:
            return item[att].lower() == 'da'
        else:
            return 0

    def process_item(self, item, spider):
        # 1. Process data
        # 2. Insert data into database

        cena = self.process_price(item)
        godiste = self.process_age(item)
        gorivo = item['gorivo']
        kubikaza = self.attribute_as_num(item['kubikaza'])
        snaga = self.attribute_as_num(item['snaga'])
        kilometraza = self.to_number(item['kilometraza'])
        tip_motora = item['tip_motora']
        pogon = item['pogon']
        tip_menjaca = item['tip_menjaca']
        broj_brzina = self.to_number(item['broj_brzina'])
        broj_vrata = item['broj_vrata']
        prosecna_potrosnja = self.to_number(item['prosecna_potrosnja'])
        ubrzanje = self.to_number(item['ubrzanje'])
        prtljaznik = item['prtljaznik']
        klima = item['klima']
        broj_sedista = self.to_number(item['broj_sedista'])
        pozicija_volana = item['pozicija_volana']
        boja = item['boja']
        boja_unutrasnjosti = item['boja_unutrasnjosti']
        kategorija_vozila = item['kategorija_vozila']

        havarisano = self.is_attribute_present(item, 'havarisano')
        garaziran = self.is_attribute_present(item, 'garaziran')
        nov = self.is_attribute_present(item, 'nov')
        servisna_knjizica = self.is_attribute_present(item, 'servisna_knjizica')
        registrovano = self.is_attribute_present(item, 'registrovano')

        if self.error_process == 0:
            cursor = self.curr.execute("""insert into car(
                naziv,
                cena,
                godiste,
                gorivo,
                kubikaza,
                snaga,
                kilometraza,
                tip_motora,
                pogon,
                tip_menjaca,
                broj_brzina,
                broj_vrata,
                prosecna_potrosnja,
                ubrzanje,
                prtljaznik,
                klima,
                broj_sedista,
                pozicija_volana,
                boja,
                boja_unutrasnjosti,
                kategorija_vozila,
                havarisano,
                garaziran,
                nov,
                servisna_knjizica,
                registrovano
              ) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                item['naziv'],
                cena,
                godiste,
                gorivo,
                kubikaza,
                snaga,
                kilometraza,
                tip_motora,
                pogon,
                tip_menjaca,
                broj_brzina,
                broj_vrata,
                prosecna_potrosnja,
                ubrzanje,
                prtljaznik,
                klima,
                broj_sedista,
                pozicija_volana,
                boja,
                boja_unutrasnjosti,
                kategorija_vozila,
                havarisano,
                garaziran,
                nov,
                servisna_knjizica,
                registrovano
            ))
        else:
            cursor = self.curr.execute("""insert into car_temp(
                naziv,
                cena,
                godiste,
                gorivo,
                kubikaza,
                snaga,
                kilometraza,
                tip_motora,
                pogon,
                tip_menjaca,
                broj_brzina,
                broj_vrata,
                prosecna_potrosnja,
                ubrzanje,
                prtljaznik,
                klima,
                broj_sedista,
                pozicija_volana,
                boja,
                boja_unutrasnjosti,
                kategorija_vozila,
                havarisano,
                garaziran,
                nov,
                servisna_knjizica,
                registrovano
              ) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                item['naziv'],
                cena,
                godiste,
                gorivo,
                kubikaza,
                snaga,
                kilometraza,
                tip_motora,
                pogon,
                tip_menjaca,
                broj_brzina,
                broj_vrata,
                prosecna_potrosnja,
                ubrzanje,
                prtljaznik,
                klima,
                broj_sedista,
                pozicija_volana,
                boja,
                boja_unutrasnjosti,
                kategorija_vozila,
                havarisano,
                garaziran,
                nov,
                servisna_knjizica,
                registrovano
            ))

        if cursor.rowcount is 0:
            self.mLogger.error("ERROR ......................................................")

        self.conn.commit()

        self.error_process = 0
        return item
