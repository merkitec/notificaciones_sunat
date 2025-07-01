# import requests
import configparser
import time
import logging
import os
from datetime import datetime

from selenium.webdriver.common.by import By

from infrastructure.selenium_rpa import SeleniumRpa
from bs4 import BeautifulSoup
import json
import pandas as pd

# Configure logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HttpSessionRpa:
    def __init__(self, headless=False, config=None):
        """        
        Initialize the Selenium WebDriver and the requests session.

        :param headless: Boolean indicating whether to run browser in headless mode.
        :param config: config.ini loaded.
        """
        self.current_cookies = []
        self.config = config
        self._automator = SeleniumRpa(headless=headless, config=config)

        # Initialize requests session
        # self.request_session = requests.Session()
        logger.info("Requests session initialized.")

    @property
    def automator(self) -> SeleniumRpa:
        return self._automator
    
    def login(self, RUC, USER, PSW):
        logger.info(f"Logging in with RUC: {RUC}")
        x_input_login_ruc = self.config["XPATHS"]["x_input_login_ruc"]
        x_input_login_user = self.config["XPATHS"]["x_input_login_user"]
        x_input_login_psw = self.config["XPATHS"]["x_input_login_psw"]
        x_bottom_login_ingreso = self.config["XPATHS"]["x_bottom_login_ingreso"]

        workflow = [
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_ruc, "text": RUC},
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_user, "text": USER},
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_psw, "text": PSW},
            {"action": "click", "by": By.XPATH, "value": x_bottom_login_ingreso, "delay": 5},
        ]
        self._automator.execute_workflow(self.config["WEBSITE"]["url_start"], workflow)
        logger.info(f"Login completed. RUC: {RUC}")

    def __modal_validation_datos(self):
        modal = self._automator.find_element(By.XPATH, self.config["XPATHS"]["x_modal_valida_datos"])
        return not modal is None
    
    def __process_modal_validation_datos(self):
        x_button_cerrar = self.config["XPATHS"]["x_modal_valida_datos_button"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_button_cerrar, "delay": 2},
        ]
        self._automator.execute_workflow("", workflow)

    def __modal_validation_datos_informativo(self):
        modal = self._automator.find_element(By.XPATH, self.config["XPATHS"]["x_modal_valida_datos_informativo"])
        return not modal is None

    def __process_modal_validation_datos_informativo(self):
        button_aceptar = self.config["XPATHS"]["x_modal_valida_datos_informativo_button"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": button_aceptar, "delay": 2},
        ]
        self._automator.execute_workflow("", workflow)

    def clear_modal_validation_datos(self):
        _iframe = self._automator.find_element(By.ID, "ifrVCE")
        if _iframe and _iframe.is_displayed() and _iframe.is_enabled():
            self._automator.driver.switch_to.frame(_iframe)

            if self.__modal_validation_datos_informativo():
                self.__process_modal_validation_datos_informativo()

            if self.__modal_validation_datos():
                self.__process_modal_validation_datos()

            self._automator.driver.switch_to.default_content()

    def open_mailbox(self, login_credentials, wait_time=5):
        self.login(login_credentials["RUC"], login_credentials["USER"], login_credentials["PSW"])

        self.clear_modal_validation_datos()
        
        # Open mailbox
        try:
            x_bottom_buzon = self.config["XPATHS"]["x_bottom_buzon"]
            workflow = [
                {"action": "click", "by": By.XPATH, "value": x_bottom_buzon, "delay": 5},
            ]
            self._automator.execute_workflow("", workflow)
            logger.info(f"Mailbox opened. RUC: {login_credentials['RUC']}")
            # self.load_info_response()
        except Exception as e:
            self.close()
            logger.error(f"Error opening mailbox: {e}")
            raise

    def close(self):
        """
        Close the Selenium WebDriver.
        """
        self._automator.quit()
        logger.info("Selenium WebDriver closed.")

    def close_extraction(self):
        x_bottom_salir = self.config["XPATHS"]["x_bottom_logout"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_bottom_salir, "delay": 5},
        ]
        self._automator.execute_workflow("", workflow)
        logger.info(f"Mailbox closed.")


if __name__ == "__main__":
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Initialize AuthenticatedSession
    session = HttpSessionRpa(headless=False, config=config)

    # Load environment variables
    credentials = {
        "RUC" : os.getenv("SUNAT_RUC"),
        "USER" : os.getenv("SUNAT_USER"),
        "PSW" : os.getenv("SUNAT_PSW"),
    }

    try:
        # Perform login
        session.open_mailbox(credentials)

        # Wait for the "quotes" divs to load
        # wait = WebDriverWait(session.automator.driver, 3)
        # notification_elements = wait.until(EC.visibility_of_element_located((By.ID, "listaMensajes")))

        notification_data = []        
        session._automator.driver.switch_to.frame(session._automator.driver.find_element(By.NAME, "iframeApplication"))
        notification_elements = session._automator.get_all_elements(By.XPATH, '//ul[@id="listaMensajes"]/li')
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
        session._automator.driver.switch_to.default_content()

        with open(f'results/notifica_{credentials["RUC"]}_{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.json', 'w') as json_file:
            json.dump(notification_data, json_file, indent=4)

        df = pd.DataFrame(notification_data)
        df.to_excel(f"results/notifica{credentials['RUC']}_{datetime.now().strftime('%Y-%m-%d %H_%M_%S')}.xlsx")

        # response = session.menu_item()       
        # session.load_info_response(response.cookies)

        # response = session.listar_carpetas()
        # session.load_info_response(response.cookies)

        # response = session.consultar_alertas()
        # session.load_info_response(response.cookies)

        # response = session.list_noti_men_pag()

    except Exception as e:
        logger.exception(e)

    finally:
        # Clean up
        session.close()
