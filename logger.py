import logging
import functools

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s") 

def errors_catching_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error("Exception", exc_info=e) 
            return e
    return wrapper