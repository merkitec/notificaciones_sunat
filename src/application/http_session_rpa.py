import requests
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
        self.request_session = requests.Session()
        logger.info("Requests session initialized.")

    @property
    def automator(self) -> SeleniumRpa:
        return self._automator
    
    def load_info_response(self, response_cookies=None):
        self.current_cookies = self._automator.driver.get_cookies()
        self.__logging_info_cookies(self.current_cookies, "Web driver cookies info:")

        # Extract cookies from Selenium and add them to requests session
        selenium_cookies = self._automator.driver.get_cookies()
        for cookie in selenium_cookies:
            self.request_session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain'), path=cookie['path'])
        logger.info("Cookies transferred to requests session.")
        self.__logging_info_cookies(self.request_session.cookies, "Transferred cookies info:")

        if not response_cookies is None:
            for cookie in response_cookies:
                self.request_session.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

        # Optionally, set headers like User-Agent to mimic the browser
        user_agent = self._automator.driver.execute_script("return navigator.userAgent;")
        self.request_session.headers.update({'User-Agent': user_agent})
        logger.info(f"User-Agent set to: {user_agent}")

    def __logging_info_cookies(self, cookies, msg):
        logger.info(msg)
        for cookie in cookies:
            logger.info(cookie)

    def login(self, RUC, USER, PSW):
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

    def open_mailbox(self, login_credentials, wait_time=5):
        self.login(login_credentials["RUC"], login_credentials["USER"], login_credentials["PSW"])

        # Wait for login to complete
        # time.sleep(wait_time)  # Adjust as necessary or implement explicit waits

        # self.load_info_response()
        
        # Open mailbox
        x_bottom_buzon = self.config["XPATHS"]["x_bottom_buzon"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_bottom_buzon, "delay": 5},
        ]
        self._automator.execute_workflow(self.config["WEBSITE"]["url_start"], workflow)
        # self.load_info_response()

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
        self._automator.execute_workflow(self.config["WEBSITE"]["url_start"], workflow)


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
