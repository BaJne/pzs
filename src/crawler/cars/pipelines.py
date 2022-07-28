# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import logging


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


class CarsPipeline:

    def __init__(self):
        self.mLogger = logging.getLogger('data.collecting')
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect(r"./../output/cars.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS car""")
        self.curr.execute("""
            CREATE TABLE car(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naziv text NOT NULL,
                cena number,
                godiste number,
                gorivo text,
                kubikaza number NULL,
                snaga number NULL,
                kilometraza number NULL,
                tip_motora text NULL,
                pogon text NULL,
                tip_menjaca text NULL,
                broj_brzina number NULL,
                broj_vrata number NULL,
                broj_sedista number NULL,
                pozicija_volana number NULL,
                klima number NULL,
                boja text NULL,
                boja_unutrasnjosti text NULL,
                kategorija_vozila text NULL,
                prosecna_potrosnja real NULL,
                ubrzanje real NULL,
                prtljaznik real NULL,
                servisna_knjizica number NULL,
                havarisano number NULL,
                garaziran number NULL,
                nov number NULL
            ) 
        """)

    def process_item(self, item, spider):
        # 1. Process data
        # 2. Insert data into database

        cena = item['cena']
        cena = remove_suffix(cena, "EUR")
        cena = cena.replace('.', '')
        cena = cena.strip()
        if cena.isnumeric():
            cena = int(cena)
        else:
            return item

        godiste = item['godiste'][0:4]

        cursor = self.curr.execute("""insert into car(naziv, cena, godiste, gorivo) values(?, ?, ?, ?)""",(
            item['naziv'],
            cena,
            godiste,
            item['gorivo']
        ))

        if cursor.rowcount is 0:
            self.mLogger.error("ERROR ......................................................")

        self.conn.commit()

        return item
