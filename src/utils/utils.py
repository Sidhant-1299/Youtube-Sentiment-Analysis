import logging

def setup_logger():
    logging.basicConfig(
        filename='data.log',
        encoding='utf-8',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s\t%(funcName)s'
    )
