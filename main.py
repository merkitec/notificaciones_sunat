from argparse import Namespace
from logging.handlers import RotatingFileHandler

from application.estudio_contable_service import EstudioContableService
from application.http_session_rpa import HttpSessionRpa
from application.notification_sunat import NotificationSunat
from infrastructure.extract_notification_manual import ExtractNotificationManual
from infrastructure.extract_notification_llm import ExtractNotificationLLM
from infrastructure.save_notification_db import SaveNotificationDb
from infrastructure.save_notification_excel import SaveNotificationExcel
from common.parameter_arguments import parse_opt
from cross_cutting.settings import Settings

import os
import pandas as pd
import logging
import configparser

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

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
        parser = parse_opt()
        args = parser.parse_args()
        logger.info(f"Args: {args}")
        settings = Settings()

        extractor = ExtractNotificationManual()
        if args.extractor == "llm":
            extractor = ExtractNotificationLLM()

        save = SaveNotificationExcel(config=config)
        if args.save_to == "db":
            save = SaveNotificationDb(config=config)

        process_sunat = NotificationSunat(
            extractor, 
            HttpSessionRpa(headless=False, config=config),
            persist=save,
            estudio_contable_svc=EstudioContableService(config=config),
            settings=settings)

        process_sunat.process_notification()

    except Exception as ex:
        logger.exception(ex)

if __name__ == "__main__":
    main()

