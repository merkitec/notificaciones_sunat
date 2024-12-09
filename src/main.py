from logging.handlers import RotatingFileHandler
from application.http_session_rpa import HttpSessionRpa
from application.extract_notification import ExtractNotification
from application.notification_sunat import NotificationSunat

import os
import pandas as pd
import logging
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("src/config.ini")

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[RotatingFileHandler('logs/my_log.log', maxBytes=1000000, backupCount=10,)],
                    datefmt='%Y-%m-%dT%H:%M:%S')
logger = logging.getLogger(__name__)
logging.getLogger("seleniumwire.server").setLevel(level=logging.WARNING)
logging.getLogger("seleniumwire.handler").setLevel(level=logging.WARNING)

   
def main():
    try:
        process_sunat = NotificationSunat(
            ExtractNotification(), 
            HttpSessionRpa(headless=False, config=config))

        process_sunat.process_notification(companies=pd.read_csv('data/credenciales_ruc.csv'))        

    except Exception as ex:
        logger.exception(ex)

if __name__ == "__main__":
    main()

