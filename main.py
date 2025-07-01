from argparse import Namespace
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from application.estudio_contable_not_found_error import EstudioContableNotFoundError
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
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[TimedRotatingFileHandler(filename='logs/my_log.log', when="midnight", backupCount=15),
                        logging.StreamHandler()],
                    datefmt='%Y-%m-%dT%H:%M:%S')
logging.getLogger("seleniumwire.server").setLevel(level=logging.WARNING)
logging.getLogger("seleniumwire.handler").setLevel(level=logging.WARNING)
logging.getLogger("hpack.hpack").setLevel(level=logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(level=logging.WARNING)
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(level=logging.WARNING)
logging.getLogger("hpack.table").setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException, Request
app = FastAPI()
@app.post("/")
async def root(request: Request):
    try:
        data = await request.json()
        ESTUDIO_CONTABLE_RUC = data.get("ESTUDIO_CONTABLE_RUC")
        if ESTUDIO_CONTABLE_RUC is None:
            raise HTTPException(status_code=400, detail="Please provide a RUC")
        os.environ["ESTUDIO_CONTABLE_RUC"] = ESTUDIO_CONTABLE_RUC
        logger.info(f"ESTUDIO_CONTABLE_RUC: {os.environ["ESTUDIO_CONTABLE_RUC"]}")
        main()
        return {"message": "Notification processing completed"}
    except EstudioContableNotFoundError as e:
        logger.exception(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as ex:
        logger.exception(str(ex))
        raise HTTPException(status_code=500, detail=str(ex))
   
def main():
    # parser = parse_opt()
    # args = parser.parse_args()
    # logger.info(f"Args: {args}")
    args_extractor = "manual"
    args_save_to = "db"
    settings = Settings()

    extractor = ExtractNotificationManual(config=config)
    # if args.extractor == "llm":
    if args_extractor == "llm":
        extractor = ExtractNotificationLLM()

    save = SaveNotificationExcel(config=config)
    # if args.save_to == "db":
    if args_save_to == "db":
        save = SaveNotificationDb(config=config)

    process_sunat = NotificationSunat(
        extractor, 
        HttpSessionRpa(headless=True, config=config),
        persist=save,
        estudio_contable_svc=EstudioContableService(config=config),
        settings=settings)

    process_sunat.process_notification()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

