from logging.handlers import RotatingFileHandler
import os
from http_session_rpa import HttpSessionRpa
import pandas as pd
import logging
from datetime import datetime
import configparser

from selenium_rpa import SeleniumRpa
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

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

def extract_notifications(session):
    notification_data = []        
    session.automator.driver.switch_to.frame(session.automator.driver.find_element(By.NAME, "iframeApplication"))
    notification_elements = session.automator.get_all_elements(By.XPATH, '//ul[@id="listaMensajes"]/li')
    # notification_elements = notification_list.find_elements_by_tag_name("li")

    for notification in notification_elements:
        logger.debug(notification.get_attribute("outerHTML"))
        soup = BeautifulSoup(notification.get_attribute("outerHTML"), 'html.parser')

        subject = soup.find('a', class_="linkMensaje text-muted").text
        publish_date = soup.find('small', class_="text-muted fecPublica").text
        id = notification.get_property('id')
        type = ""
        if len(soup.select('div>span[class*="label tag"]')) > 0:
            type = soup.select('div>span[class*="label tag"]')[0].text

        notification_info = {
            "id": id,
            "subject": subject,
            "publish_date": publish_date,
            "type": type
        }
        notification_data.append(notification_info)
    session.automator.driver.switch_to.default_content()

    return notification_data

def save_results(file_path, notifications, id_name_part):   
    os.makedirs(file_path, exist_ok=True)
    with open(f'{file_path}/notifica_{id_name_part}_{datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}.json', 'w') as json_file:
        json.dump(notifications, json_file, indent=4)

    df = pd.DataFrame(notifications)
    df.to_excel(f"{file_path}/notifica_{id_name_part}_{datetime.now().strftime('%Y.%m.%d_%H.%M.%S')}.xlsx")

    
def main():
    try:
        session = HttpSessionRpa(headless=False, config=config)
        credenciales = pd.read_csv('data/credenciales_ruc.csv')

        for idx, credencial in credenciales.iterrows():
            session.open_mailbox(credencial)
            notifications = extract_notifications(session)
            session.close_extraction()

            save_results('./results', notifications, credencial['RUC'])

    except Exception as ex:
        logger.exception(ex)

    finally:
        # Clean up
        session.close()

if __name__ == "__main__":
    main()

