import requests
import configparser
import time
import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium_rpa import SeleniumRpa

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Load environment variables
RUC = os.getenv("SUNAT_RUC")
USER = os.getenv("SUNAT_USER")
PSW = os.getenv("SUNAT_PSW")

class HttpSessionRpa:
    def __init__(self, headless=False):
        """
        Initialize the Selenium WebDriver and the requests session.

        :param driver_path: Path to the WebDriver executable.
        :param headless: Boolean indicating whether to run browser in headless mode.
        """
        self.automator = SeleniumRpa(headless=headless)

        # Initialize requests session
        self.session = requests.Session()
        logger.info("Requests session initialized.")

    def login(self):
        x_input_login_ruc = config["XPATHS"]["x_input_login_ruc"]
        x_input_login_user = config["XPATHS"]["x_input_login_user"]
        x_input_login_psw = config["XPATHS"]["x_input_login_psw"]
        x_bottom_login_ingreso = config["XPATHS"]["x_bottom_login_ingreso"]

        workflow = [
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_ruc, "text": RUC},
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_user, "text": USER},
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_psw, "text": PSW},
            {"action": "click", "by": By.XPATH, "value": x_bottom_login_ingreso, "delay": 10},
        ]
        self.automator.execute_workflow(config["WEBSITE"]["url_start"], workflow)

    def open_mailbox(self, wait_time=5):
        """
        Perform login using Selenium WebDriver.

        :param wait_time: Time to wait after login (in seconds).
        """
        self.login()

        # Wait for login to complete
        time.sleep(wait_time)  # Adjust as necessary or implement explicit waits

        # Extract cookies from Selenium and add them to requests session
        selenium_cookies = self.automator.driver.get_cookies()
        for cookie in selenium_cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain'))
        logger.info("Cookies transferred to requests session.")

        # Optionally, set headers like User-Agent to mimic the browser
        user_agent = self.automator.driver.execute_script("return navigator.userAgent;")
        self.session.headers.update({'User-Agent': user_agent})
        logger.info(f"User-Agent set to: {user_agent}")

        # Open mailbox
        x_bottom_buzon = config["XPATHS"]["x_bottom_buzon"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_bottom_buzon, "delay": 20},
        ]
        self.automator.execute_workflow(config["WEBSITE"]["url_start"], workflow)

    def make_post_request(self, url, data, headers=None):
        """
        Make an HTTP POST request using the authenticated requests session.

        :param url: The URL to send the POST request to.
        :param data: Dictionary containing the POST data.
        :param headers: (Optional) Dictionary containing additional headers.
        :return: Response object.
        """
        if headers:
            # Merge the session headers with additional headers
            combined_headers = self.session.headers.copy()
            combined_headers.update(headers)
        else:
            combined_headers = self.session.headers

        logger.info(f"Making POST request to {url} with data {data} and headers {combined_headers}")
        response = self.session.post(url, data=data, headers=combined_headers)
        logger.info(f"Received response with status code {response.status_code}")
        return response

    def close(self):
        """
        Close the Selenium WebDriver.
        """
        self.automator.quit()
        logger.info("Selenium WebDriver closed.")

if __name__ == "__main__":
    # Initialize AuthenticatedSession
    session = HttpSessionRpa()

    try:
        # Perform login
        session.open_mailbox()

        # Make a POST request after login
        POST_URL = config["WEBSITE"]["url_start"]
        POST_DATA = {
            "action": "prevApp"
        }
        ADDITIONAL_HEADERS = {
            "Content-Type": "application/x-www-form-urlencoded"  # Example header
        }

        response = session.make_post_request(url=POST_URL, data=POST_DATA, headers=ADDITIONAL_HEADERS)

        # Process the response
        if response.ok:
            logger.info("POST request successful.")
            logger.info(f"Response Data: {response.text}")
        else:
            logger.error(f"POST request failed with status code {response.status_code}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        # Clean up
        session.close()
