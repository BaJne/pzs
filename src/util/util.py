import logging
import sys

FORMAT = '%(filename)s[%(funcName)s:%(lineno)d] | %(levelname)s: %(message)s'


def get_file_handler(fmt):
    file_handler = logging.FileHandler('./../output/log')
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_stream_handler(fmt):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)
    stream_handler.setLevel(logging.DEBUG)
    return stream_handler


def init_logger(name):
    fmt = logging.Formatter(fmt=FORMAT)
    logger = logging.getLogger(name)
    logger.addHandler(get_stream_handler(fmt))
    logger.addHandler(get_file_handler(fmt))
    logger.setLevel(logging.DEBUG)
