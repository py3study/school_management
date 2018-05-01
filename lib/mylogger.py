import logging
from conf import settings
class Logger:
    logger = logging.getLogger()
    fh = logging.FileHandler(settings.file_name['log_path'],encoding='utf-8',mode='a')
    #ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    #ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #logger.addHandler(ch)
