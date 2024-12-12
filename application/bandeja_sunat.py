import os
import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
RUC = os.getenv("SUNAT_RUC")
USER = os.getenv("SUNAT_USER")
PSW = os.getenv("SUNAT_PSW")

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

import requests

def post_to_sunat(url, cookies):
    """
    Makes an HTTP POST request to the given URL with specified headers and cookies.

    :param url: The URL to make the POST request to.
    :param cookies: A dictionary of cookies to include in the request.
    :return: The response object from the request.
    """
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "host": "e-menu.sunat.gob.pe",
        "origin": "https://e-menu.sunat.gob.pe",
        "referer": "https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm?pestana=*&agrupacion=*",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }

    # Example payload, update as required
    payload = {
        "action": "prevApp"
    }
    cookie_hdr = "".join(["".join([f"{key}={value[k]}; " for k in value if k == 'value']) for key, value in cookies.items()])
    try:
        response = requests.post(url, headers=headers, cookies=cookie_hdr, data=payload)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        return response
    except requests.RequestException as e:
        print("An error occurred during the POST request:", e)
        return None
    
def get_all_cookies(driver):
    """
    Retrieves all cookies from the browser session.
    
    :param driver: Selenium WebDriver instance
    :return: Dictionary of cookies with cookie names as keys and their attributes as values
    """
    cookies = driver.get_cookies()
    return {cookie['name']: cookie for cookie in cookies}

def make_post_request(driver, post_url, data):
    # Get the request from the login process
    requests = driver.requests

    # Find the request that matches the login request (adjust the filter as needed)
    login_request = next(r for r in requests if r.response.status_code == 200 and r.url == config["WEBSITE"]["url_start"])

    # Extract headers and cookies
    headers = login_request.headers
    cookies = login_request.cookies

    # Make the POST request with the extracted headers and cookies
    response = requests.post(post_url, headers=headers, cookies=cookies, data=data)

    return response


def main():
    # Ensure credentials are set
    if not all([RUC, USER, PSW]):
        raise ValueError("Environment variables for login credentials are not set!")

    # Load URL and XPath from config.ini
    url_start = config["WEBSITE"]["url_start"]
    x_input_login_ruc = config["XPATHS"]["x_input_login_ruc"]
    x_input_login_user = config["XPATHS"]["x_input_login_user"]
    x_input_login_psw = config["XPATHS"]["x_input_login_psw"]
    x_bottom_login_ingreso = config["XPATHS"]["x_bottom_login_ingreso"]
    x_bottom_buzon = config["XPATHS"]["x_bottom_buzon"]
    user_data_dir = config["TEMP"]["user_data_dir"]

    # Selenium options
    opciones = webdriver.ChromeOptions()
    opciones.add_experimental_option("excludeSwitches", ['enable-automation'])
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    opciones.add_experimental_option("prefs", prefs)
    opciones.add_argument(f"user-data-dir={user_data_dir}")
    
    # Initialize the browser driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opciones)
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)

    try:
        # Open the SUNAT login page
        driver.get(url_start)

        # Enter login details
        wait.until(ec.visibility_of_element_located((By.XPATH, x_input_login_ruc)))
        driver.find_element(By.XPATH, x_input_login_ruc).send_keys(RUC)
        driver.find_element(By.XPATH, x_input_login_user).send_keys(USER)
        driver.find_element(By.XPATH, x_input_login_psw).send_keys(PSW)
        time.sleep(0.7)

        # Submit login form
        driver.find_element(By.XPATH, x_bottom_login_ingreso).click()

        # Navigate to "Buzón"
        wait.until(ec.element_to_be_clickable((By.XPATH, x_bottom_buzon)))
        driver.find_element(By.XPATH, x_bottom_buzon).click()
        
        time.sleep(10)

        # Get all cookies
        cookies = get_all_cookies(driver)
        print("Retrieved Cookies:", cookies)

        # Post menu=buzon to get the final cookies
        payload = {
            "action": "prevApp"
        }
        # response = post_to_sunat(url_start, cookies)
        response = make_post_request(driver, url_start, payload)
        print(response)

        # Get all last cookies
        cookies = get_all_cookies(driver)

        # Post https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/consultarAlertas

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
