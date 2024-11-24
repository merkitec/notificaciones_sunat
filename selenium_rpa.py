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
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Load environment variables
RUC = os.getenv("SUNAT_RUC")
USER = os.getenv("SUNAT_USER")
PSW = os.getenv("SUNAT_PSW")

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("seleniumwire.server").setLevel(level=logging.INFO)
logging.getLogger("seleniumwire.handler").setLevel(level=logging.INFO)

class SeleniumRpa:
    def __init__(self, browser="chrome", options=None, timeout=30, headless=False):
        """
        Initializes the web scraper with Selenium WebDriver.

        :param browser: The browser to use ("chrome" or "firefox"). Default is "chrome".
        :param options: Browser options. Default is None.
        :param timeout: Timeout for waiting on elements. Default is 30 seconds.
        """
        print("Python version:", platform.python_version())
        print("Architecture:", platform.architecture())
        print("Processor Arch:", os.environ["PROCESSOR_ARCHITECTURE"])

        if browser.lower() == "chrome":
            options = options or webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")     

            self._driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=options
            )
        elif browser.lower() == "firefox":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager

            options = options or webdriver.FirefoxOptions()
            self._driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=options
            )
        else:
            raise ValueError("Unsupported browser. Use 'chrome' or 'firefox'.")
        logger.info("Selenium WebDriver initialized.")

        self._driver.maximize_window()
        self.wait = WebDriverWait(self._driver, timeout)

    @property
    def driver(self):
        return self._driver
    
    def open_page(self, url):
        """
        Opens the specified webpage.

        :param url: The URL to open.
        """
        self._driver.get(url)

    def wait_and_get_element(self, by, value):
        """
        Waits for an element to be visible and returns it.

        :param by: Locator strategy (e.g., By.XPATH, By.ID).
        :param value: The locator value.
        :return: The WebElement.
        """
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def wait_and_get_elements(self, by, value):
        """
        Waits for an element to be visible and returns it.

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
        Gets the text content of an element.

        :param by: Locator strategy.
        :param value: The locator value.
        :return: The element.
        """
        element = self.wait_and_get_element(by, value)
        return element

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
        General-purpose scraping method to navigate and extract data.

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
            elif action_type == "click":
                self.click_element(by, value)
            elif action_type == "enter_text":
                self.enter_text(by, value, action["text"])
            time.sleep(action.get("delay", 1))  # Optional delay
        return data

    def execute_workflow(self, url, tasks):
        """
        Automates a workflow based on a sequence of tasks.

        :param url: The URL to start automation.
        :param tasks: A list of tasks (e.g., "click", "enter_text").
        """
        self.open_page(url)
        for task in tasks:
            action = task["action"]
            by = task.get("by")
            value = task.get("value")
            if action == "click":
                self.click_element(by, value)
            elif action == "enter_text":
                self.enter_text(by, value, task["text"])
            elif action == "navigate":
                self.open_page(task["url"])
            time.sleep(task.get("delay", 1))  # Optional delay between actions

    def quit(self):
        """Closes the browser and ends the session."""
        self._driver.quit()

def login(automator):
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

# Example Usage
if __name__ == "__main__":
    automator = SeleniumRpa()
    try:
        # actions = [
        #     {"type": "get_text", "name": "title", "by": By.TAG_NAME, "value": "h1"},
        #     {"type": "click", "by": By.LINK_TEXT, "value": "About"},
        #     {"type": "get_text", "name": "about", "by": By.TAG_NAME, "value": "p"},
        # ]
        login(automator)

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
    finally:
        automator.quit()
