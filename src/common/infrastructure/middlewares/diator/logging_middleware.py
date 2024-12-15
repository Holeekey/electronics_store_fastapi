from diator.requests.request import Request

from common.infrastructure.loggers.loguru_logger import LoguruLogger


class LoggingMiddleware:
    
    async def __call__(self, request: Request, handle):
        
        logger = LoguruLogger(handle.__class__.__name__)
        
        logger.log('INPUT', request)
        
        try:
            response = await handle(request)
            logger.log('OUTPUT', response)
            return response
        except Exception as e:
            logger.error(e)
            raise e
