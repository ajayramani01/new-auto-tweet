import logging
logger = logging.getLogger(__name__)
from .utils import opendriver
from datetime import datetime,date
def tweetJob():
    today = date.today()
    if today.weekday() in [0,1,2,3,4]:
        opendriver()
        
    else:
        logger.info("Holiday")