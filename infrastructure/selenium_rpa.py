import os
import time
import configparser
import platform

# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeleniumRpa:
    def __init__(self, browser="chrome", options=None, timeout=60, headless=False, config=None):
        """
        Initializes the web scraper with Selenium WebDriver.

        :param browser: The browser to use ("chrome" or "firefox"). Default is "chrome".
        :param options: Browser options. Default is None.
        :param timeout: Timeout for waiting on elements. Default is 30 seconds.
        """
        logger.info(f"Python version: {platform.python_version()}")
        logger.info(f"Architecture: {platform.architecture()}")
        if 'PROCESSOR_ARCHITECTURE' in os.environ:
            logger.info(f"Processor Arch: {os.environ['PROCESSOR_ARCHITECTURE']}")

        if browser.lower() == "chrome":
            # options = options or webdriver.ChromeOptions()
            # if headless:
            #     options.add_argument("--headless")
            # options.add_argument("--disable-gpu")
            # options.add_argument("--no-sandbox")     
            # options.add_argument('--disable-dev-shm-usage')
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--window-size=1680,1280")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            # options.add_experimental_option("excludeSwitches",['enable-automation'])
            # prefs = {"credentials_enable_service": False,"profile.password_manager_enabled": False}
            # options.add_experimental_option("prefs", prefs)
            # # options.add_argument("user-data-dir=C:\\Users\\ytamayo\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")
            # options.add_argument(f"user-data-dir={config['TEMP']['user_data_dir']}")

            # self._driver = webdriver.Chrome(
            #     service=ChromeService(ChromeDriverManager().install()), options=options)
            self._driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), 
                options=chrome_options)
            logger.info(f"Chrome Driverversion: {self._driver.capabilities['chrome']['chromedriverVersion'].split(' ')}")

        elif browser.lower() == "firefox":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager

            options = options or webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            self._driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=options
            )
        else:
            raise ValueError("Unsupported browser. Use 'chrome' or 'firefox'.")
        logger.info("Selenium WebDriver initialized.")

        # self._driver.maximize_window()
        self.wait = WebDriverWait(self._driver, timeout)
        self.config = config

    @property
    def driver(self):
        return self._driver
    
    def open_page(self, url):
        """
        Opens the specified webpage.

        :param url: The URL to open.
        """
        self._driver.get(url)
        logger.info(f"Opened page: {url}")

    def wait_and_get_element(self, by, value):
        """
        Waits for an element to be visible and returns it.

        :param by: Locator strategy (e.g., By.XPATH, By.ID).
        :param value: The locator value.
        :return: The WebElement.
        """
        logger.debug(f"Waiting for element: {by} - {value}")
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def wait_and_get_elements(self, by, value):
        """
        Waits for elements to be visible and returns it.

        :param by: Locator strategy (e.g., By.XPATH, By.ID).
        :param value: The locator value.
        :return: The WebElement.
        """
        return self.wait.until(EC.visibility_of_all_elements_located((by, value)))

    def get_text(self, by, value):
        """
        Gets the text content of an element.

        :param by: Locator strategy.
        :param value: The locator value.
        :return: The text content of the element.
        """
        element = self.wait_and_get_element(by, value)
        return element.text

    def get_element(self, by, value):
        """
        Gets the web element.

        :param by: Locator strategy.
        :param value: The locator value.
        :return: The element.
        """
        element = self.wait_and_get_element(by, value)
        return element

    def find_element(self, by, value):
        """
        Finds an element.

        :param by: Locator strategy.
        :param value: The locator value.
        :return: The element.
        """
        try:
            element = self._driver.find_element(by, value)
            return element
        except Exception as e:
            logger.error("Error finding element: %s", e)
            return None

    def find_elements(self, by, value):
        """
        Finds all elements.

        :param by: Locator strategy.
        :param value: The locator value.
        :return: The elements.
        """
        try:
            elements = self._driver.find_elements(by, value)
            return elements
        except Exception as e:
            logger.error("Error finding elements: %s", e)
            return []


    def get_all_elements(self, by, value):
        """
        Gets all the elements of a HTML Tag.

        :param by: Locator strategy.
        :param value: The locator value.
        :return: The elements.
        """
        element = self.wait_and_get_elements(by, value)
        return element

    def click_element(self, by, value):
        """
        Waits for an element to be clickable and clicks it.

        :param by: Locator strategy.
        :param value: The locator value.
        """
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def enter_text(self, by, value, text):
        """
        Waits for an input element and sends text to it.

        :param by: Locator strategy.
        :param value: The locator value.
        :param text: The text to input.
        """
        element = self.wait_and_get_element(by, value)
        element.clear()
        element.send_keys(text)

    def scrape(self, url, actions):
        """
        General-purpose scraping method to navigate and extract data. (reuse execute_workflow)

        :param url: The URL to scrape.
        :param actions: A list of actions (e.g., "click", "get_text", "enter_text").
        :return: Extracted data.
        """
        self.open_page(url)
        data = {}

        for action in actions:
            action_type = action["type"]
            by = action.get("by")
            value = action.get("value")

            if action_type == "get_text":
                data[action["name"]] = self.get_text(by, value)
            else:
                self.execute_workflow(url, actions)

            time.sleep(action.get("delay", 1))  # Optional delay
        return data

    def execute_workflow(self, url, tasks):
        """
        Automates a workflow based on a sequence of tasks.

        :param url: The URL to start automation.
        :param tasks: A list of tasks (e.g., "click", "enter_text").
        """
        if len(url.strip()) > 0:
            self.open_page(url)

        for task in tasks:
            action_type = task["action"]
            by = task.get("by")
            value = task.get("value")

            if action_type == "click":
                self.click_element(by, value)
            elif action_type == "enter_text":
                self.enter_text(by, value, task["text"])
            # elif action_type == "enter_text":
            #     self.enter_text(by, value, action_type["text"])
            elif action_type == "navigate":
                self.open_page(task["url"])

            time.sleep(task.get("delay", 2))  # Optional delay between actions

    def quit(self):
        """Closes the browser and ends the session."""
        self._driver.quit()
        logger.info("Selenium WebDriver closed.")

# Example Usage
if __name__ == "__main__":

    # Load environment variables
    RUC = os.getenv("SUNAT_RUC")
    USER = os.getenv("SUNAT_USER")
    PSW = os.getenv("SUNAT_PSW")

    def login(automator, config):
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
        automator.execute_workflow(config["WEBSITE"]["url_start"], workflow)

    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    automator = SeleniumRpa()
    try:
        login(automator, config)

        x_bottom_logout = config["XPATHS"]["x_bottom_logout"]
        x_bottom_buzon = config["XPATHS"]["x_bottom_buzon"]
        user_data_dir = config["TEMP"]["user_data_dir"]
        
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_bottom_buzon, "delay": 20},
            {"action": "click", "by": By.XPATH, "value": x_bottom_logout, "delay": 10},
            # {"action": "navigate", "url": "https://example.com/logout"},
        ]
        # data = scraper.scrape(config["WEBSITE"]["url_start"], actions)
        automator.execute_workflow(config["WEBSITE"]["url_start"], workflow)

        # print("Scraped Data:", data)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        automator.quit()
