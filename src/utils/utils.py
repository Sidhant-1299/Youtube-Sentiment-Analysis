import logging

def setup_logger(name = __name__, log_file = 'data.log'):
    logger = logging.getLogger(name)
    logging.basicConfig(
        filename=log_file,
        encoding='utf-8',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(levelname)s\t%(asctime)s\t%(message)s\t%(funcName)s'
    )
    return logger