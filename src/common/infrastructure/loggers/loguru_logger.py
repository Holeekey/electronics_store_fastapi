import sys
from common.application.logger.logger import ILogger
from loguru import logger

class LoguruLogger(ILogger):
    
    def __init__(self, title: str) -> None:
        logger.remove()
        logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>")
        self.title = title
    
    def log(self, *args) -> None:
        message = '[' + self.title + '] ' + ' - '.join(map(str, args))
        logger.info(message)

    def error(self, *args) -> None:
        message = '[' + self.title + '] ' +  'ERROR - ' + ' - '.join(map(str, args))
        logger.error(message)

    def exception(self, *args) -> None:
        message = '[' + self.title + '] ' + 'EXCEPTION - ' + ' - '.join(map(str, args))
        logger.error(message)