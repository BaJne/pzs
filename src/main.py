from scrapy.crawler import CrawlerProcess
from crawler.cars.spiders.car_spider import CarSpider
from crawler.cars.settings import FEED_FORMAT, FEED_EXPORT_ENCODING, ITEM_PIPELINES, USER_AGENT
import numpy as np
import os
import time
import logging
from util.util import init_logger, FORMAT

FEED_URI = "./../output/cars_"


def generate_filename():
    file_path = FEED_URI + str(np.random.randint(low=0, high=10000)) + '.json'
    return file_path


if __name__ == '__main__':
    if not os.path.isdir(r"./../output"):
        os.makedirs("./../output")

    init_logger('data.collecting')
    logger = logging.getLogger('data.collecting')
    logger.debug('Start scraping.. ')

    filename = generate_filename()
    while os.path.exists(filename):
        filename = generate_filename()

    logger.debug('Generated Json filename: %s', filename)

    t1 = time.time()

    c = CrawlerProcess({
        'FEED_FORMAT': FEED_FORMAT,
        'FEED_URI': filename,
        'FEED_EXPORT_ENCODING': FEED_EXPORT_ENCODING,
        'ITEM_PIPELINES': ITEM_PIPELINES,
        'USER_AGENT': USER_AGENT,
        'LOG_FILE': './../output/log',
        'LOG_FORMAT': FORMAT,
        'LOG_LEVEL': logging.WARNING
    })
    c.crawl(CarSpider)
    c.start()

    t2 = time.time()

    logger.debug('Time elapsed: ' + str(t2 - t1))
