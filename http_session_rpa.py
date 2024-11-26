import requests
import configparser
import time
import logging
import os
from datetime import datetime

from selenium.webdriver.common.by import By

from selenium_rpa import SeleniumRpa
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

        :param driver_path: Path to the WebDriver executable.
        :param headless: Boolean indicating whether to run browser in headless mode.
        """
        self.current_cookies = []
        self.config = config
        self.automator = SeleniumRpa(headless=headless)

        # Initialize requests session
        self.session = requests.Session()
        logger.info("Requests session initialized.")

    def load_info_response(self, response_cookies=None):
        self.current_cookies = self.automator.driver.get_cookies()
        self.__logging_info_cookies(self.current_cookies, "Web driver cookies info:")

        # Extract cookies from Selenium and add them to requests session
        selenium_cookies = self.automator.driver.get_cookies()
        for cookie in selenium_cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain'), path=cookie['path'])
        logger.info("Cookies transferred to requests session.")
        self.__logging_info_cookies(self.session.cookies, "Transferred cookies info:")

        if not response_cookies is None:
            for cookie in response_cookies:
                self.session.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

        # Optionally, set headers like User-Agent to mimic the browser
        user_agent = self.automator.driver.execute_script("return navigator.userAgent;")
        self.session.headers.update({'User-Agent': user_agent})
        logger.info(f"User-Agent set to: {user_agent}")

    def __logging_info_cookies(self, cookies, msg):
        logger.info(msg)
        for cookie in cookies:
            logger.info(cookie)

    def make_post_request(self, post_url, data):
        # Get the requests history
        all_requests = self.driver.requests

        # Get the last request and its response
        last_request = all_requests[-1]
        last_response = last_request.response

        # Combine cookies from both request and response
        all_cookies = last_request.cookies.copy()
        for cookie in last_response.cookies:
            all_cookies[cookie.name] = cookie.value

        # Make the POST request with the combined cookies and headers
        response = requests.post(post_url, headers=last_request.headers, cookies=all_cookies, data=data)

        # Update the driver's cookies with the new cookies from the response
        for cookie in response.cookies:
            self.driver.add_cookie({'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain, 'path': cookie.path, 'expiry': cookie.expiry})

        return response

    def make_post_request(self, url, data, headers=None, cookies=None):
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
        self.__logging_info_cookies(self.session.cookies, f"POST {url} Requests.session cookies info:")

        response = self.session.post(url, data=data, headers=combined_headers)
        logger.info(f"Received response with status code {response.status_code}")
        return response

    def make_get_request(self, url, data, headers=None, cookies=None):
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

        logger.info(f"Making GET request to {url} with data {data} and headers {combined_headers}")
        self.__logging_info_cookies(self.session.cookies, f"GET {url} Requests.session cookies info:")

        response = self.session.get(url, data=data, headers=combined_headers)
        logger.info(f"Received response with status code {response.status_code}")
        return response

    def login(self, RUC, USER, PSW):
        x_input_login_ruc = self.config["XPATHS"]["x_input_login_ruc"]
        x_input_login_user = self.config["XPATHS"]["x_input_login_user"]
        x_input_login_psw = self.config["XPATHS"]["x_input_login_psw"]
        x_bottom_login_ingreso = self.config["XPATHS"]["x_bottom_login_ingreso"]

        workflow = [
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_ruc, "text": RUC},
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_user, "text": USER},
            {"action": "enter_text", "by": By.XPATH, "value": x_input_login_psw, "text": PSW},
            {"action": "click", "by": By.XPATH, "value": x_bottom_login_ingreso, "delay": 10},
        ]
        self.automator.execute_workflow(self.config["WEBSITE"]["url_start"], workflow)

    def open_mailbox(self, login_credentials, wait_time=5):
        self.login(login_credentials["RUC"], login_credentials["USER"], login_credentials["PSW"])

        # Wait for login to complete
        time.sleep(wait_time)  # Adjust as necessary or implement explicit waits

        self.load_info_response()
        
        # Open mailbox
        x_bottom_buzon = self.config["XPATHS"]["x_bottom_buzon"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_bottom_buzon, "delay": 6},
        ]
        self.automator.execute_workflow(self.config["WEBSITE"]["url_start"], workflow)
        self.load_info_response()

    def close(self):
        """
        Close the Selenium WebDriver.
        """
        self.automator.quit()
        logger.info("Selenium WebDriver closed.")

    def menu_item(self):
        # Make a POST request : MenuInternet.htm
        POST_URL = self.config["WEBSITE"]["url_start"]
        POST_DATA = {
            "action": "prevApp"
        }
        ADDITIONAL_HEADERS = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "e-menu.sunat.gob.pe",
            "Origin": "https://e-menu.sunat.gob.pe",
            # "Referer": "https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm?pestana=*&agrupacion=*",
            "Sec-Ch-Ua": 'Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        response = session.make_post_request(url=POST_URL, data=POST_DATA, headers=ADDITIONAL_HEADERS)      

        # Process the response: MenuInternet.htm
        if response.ok:
            logger.info("POST request successful.")
            logger.info(f"Response Data: {response.text}")
        else:
            logger.error(f"POST request failed with status code {response.status_code}")

        return response

    def listar_carpetas(self):
        # Make a GET request : listarCarpetas
        POST_URL = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/ajax/listarCarpetas?_=1732302915481"
        POST_DATA = {
            "_":"1732302915482"
        }
        ADDITIONAL_HEADERS = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-language": "en-US,en;q=0.9,es;q=0.8",
            "Host": "ww1.sunat.gob.pe",
            "Referer": "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/master?hc=9800d69758bbdd9790a73f5c400fca03efed21f8&token=rO0ABXNyAC1wZS5nb2Iuc3VuYXQudGVjbm9sb2dpYS5tZW51LmJlYW4uVXN1YXJpb0JlYW6pwYmu%2FJtYOAIAFFMAB25pdmVsVU9MAAphcGVNYXRlcm5vdAASTGphdmEvbGFuZy9TdHJpbmc7TAAKYXBlUGF0ZXJub3EAfgABTAAHY29kQ2F0ZXEAfgABTAAJY29kRGVwZW5kcQB%2BAAFMAAxjb2RUT3BlQ29tZXJxAH4AAUwABWNvZFVPcQB%2BAAFMAAZjb3JyZW9xAH4AAUwAB2Rlc0NhdGVxAH4AAUwABWRlc1VPcQB%2BAAFMAAJpZHEAfgABTAAJaWRDZWx1bGFycQB%2BAAFMAAVsb2dpbnEAfgABTAADbWFwdAAPTGphdmEvdXRpbC9NYXA7TAAObm9tYnJlQ29tcGxldG9xAH4AAUwAB25vbWJyZXNxAH4AAUwAC25yb1JlZ2lzdHJvcQB%2BAAFMAAZudW1SVUNxAH4AAUwABnRpY2tldHEAfgABTAAKdXN1YXJpb1NPTHEAfgABeHAAAHQAAHQAAHQAAHQABDAwMjN0AAB0AAB0AAB0AAB0AAB0AAB0AAEtdAATMjA2MDYyMDg0MTRBTExPREFOU3NyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAAKdAAHZGRwRGF0YXNxAH4AED9AAAAAAAAMdwgAAAAQAAAACXQACXQxMjM4X2VtcHQAATB0AApkZHBfZXN0YWRvdAACMDB0AApkZHBfdHBvZW1wdAACMzl0AApkZHBfZmxhZzIydAACMDB0AApkZHBfbnVtcmVndAAEMDAyM3QACmRkcF91YmlnZW90AAYxNTAxMzV0AApkZHBfdGFtYW5vdAACMDN0AAhkZHBfY2lpdXQABTc0MTQ1dAAKZGRwX251bXJ1Y3QACzIwNjA2MjA4NDE0eHQACXRpcE9yaWdlbnQAAklUdAAFcm9sZXNzcQB%2BABA%2FQAAAAAAAEHcIAAAAEAAAAAB4dAAKdGlwVXN1YXJpb3QAATB0AAZpZE1lbnV0AA0xMzI3MTQxNDUxOTk0dAAIam5kaVBvb2x0AAVwMDAyM3QADnZpZ0ludm9jYUhhc3Rhc3IADmphdmEubGFuZy5Mb25nO4vkkMyPI98CAAFKAAV2YWx1ZXhyABBqYXZhLmxhbmcuTnVtYmVyhqyVHQuU4IsCAAB4cAAAAZNVVhv4dAAOdmlnSW52b2NhRGVzZGVzcQB%2BADEAAAGTVUwJ2HQABmlzQ2xvbnNyABFqYXZhLmxhbmcuQm9vbGVhbs0gcoDVnPruAgABWgAFdmFsdWV4cAB0AAxwcmltZXJBY2Nlc29zcQB%2BADcBeHQAEU1FUktJIFBFUlUgUy5BLkMudAARTUVSS0kgUEVSVSBTLkEuQy50AAB0AAsyMDYwNjIwODQxNHQAEzEzMjcxNDE0NTE5OTQtYnV6b250AAhBTExPREFOUw%3D%3D",
            "Sec-Ch-Ua": 'Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Ruc": "20606208414"
        }
        response = session.make_get_request(url=POST_URL, data=POST_DATA, headers=ADDITIONAL_HEADERS)      

        # Process the response: consultarAlertas
        if response.ok:
            logger.info("POST request successful.")
            logger.info(f"Response Data: {response.text}")
        else:
            logger.error(f"POST request failed with status code {response.status_code}")

        return response

    def consultar_alertas(self):
        # Make a POST request : consultarAlertas
        POST_URL = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/consultarAlertas"
        POST_DATA = ""
        ADDITIONAL_HEADERS = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-language": "en-US,en;q=0.9,es;q=0.8",
            "Host": "ww1.sunat.gob.pe",
            "Origin": "https://ww1.sunat.gob.pe",
            "Referer": "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/master?hc=9800d69758bbdd9790a73f5c400fca03efed21f8&token=rO0ABXNyAC1wZS5nb2Iuc3VuYXQudGVjbm9sb2dpYS5tZW51LmJlYW4uVXN1YXJpb0JlYW6pwYmu%2FJtYOAIAFFMAB25pdmVsVU9MAAphcGVNYXRlcm5vdAASTGphdmEvbGFuZy9TdHJpbmc7TAAKYXBlUGF0ZXJub3EAfgABTAAHY29kQ2F0ZXEAfgABTAAJY29kRGVwZW5kcQB%2BAAFMAAxjb2RUT3BlQ29tZXJxAH4AAUwABWNvZFVPcQB%2BAAFMAAZjb3JyZW9xAH4AAUwAB2Rlc0NhdGVxAH4AAUwABWRlc1VPcQB%2BAAFMAAJpZHEAfgABTAAJaWRDZWx1bGFycQB%2BAAFMAAVsb2dpbnEAfgABTAADbWFwdAAPTGphdmEvdXRpbC9NYXA7TAAObm9tYnJlQ29tcGxldG9xAH4AAUwAB25vbWJyZXNxAH4AAUwAC25yb1JlZ2lzdHJvcQB%2BAAFMAAZudW1SVUNxAH4AAUwABnRpY2tldHEAfgABTAAKdXN1YXJpb1NPTHEAfgABeHAAAHQAAHQAAHQAAHQABDAwMjN0AAB0AAB0AAB0AAB0AAB0AAB0AAEtdAATMjA2MDYyMDg0MTRBTExPREFOU3NyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAAKdAAHZGRwRGF0YXNxAH4AED9AAAAAAAAMdwgAAAAQAAAACXQACXQxMjM4X2VtcHQAATB0AApkZHBfZXN0YWRvdAACMDB0AApkZHBfdHBvZW1wdAACMzl0AApkZHBfZmxhZzIydAACMDB0AApkZHBfbnVtcmVndAAEMDAyM3QACmRkcF91YmlnZW90AAYxNTAxMzV0AApkZHBfdGFtYW5vdAACMDN0AAhkZHBfY2lpdXQABTc0MTQ1dAAKZGRwX251bXJ1Y3QACzIwNjA2MjA4NDE0eHQACXRpcE9yaWdlbnQAAklUdAAFcm9sZXNzcQB%2BABA%2FQAAAAAAAEHcIAAAAEAAAAAB4dAAKdGlwVXN1YXJpb3QAATB0AAZpZE1lbnV0AA0xMzI3MTQxNDUxOTk0dAAIam5kaVBvb2x0AAVwMDAyM3QADnZpZ0ludm9jYUhhc3Rhc3IADmphdmEubGFuZy5Mb25nO4vkkMyPI98CAAFKAAV2YWx1ZXhyABBqYXZhLmxhbmcuTnVtYmVyhqyVHQuU4IsCAAB4cAAAAZNVVhv4dAAOdmlnSW52b2NhRGVzZGVzcQB%2BADEAAAGTVUwJ2HQABmlzQ2xvbnNyABFqYXZhLmxhbmcuQm9vbGVhbs0gcoDVnPruAgABWgAFdmFsdWV4cAB0AAxwcmltZXJBY2Nlc29zcQB%2BADcBeHQAEU1FUktJIFBFUlUgUy5BLkMudAARTUVSS0kgUEVSVSBTLkEuQy50AAB0AAsyMDYwNjIwODQxNHQAEzEzMjcxNDE0NTE5OTQtYnV6b250AAhBTExPREFOUw%3D%3D",
            "Sec-Ch-Ua": 'Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Ruc": "20606208414"
        }
        response = session.make_post_request(url=POST_URL, data=POST_DATA, headers=ADDITIONAL_HEADERS)      

        session.load_info_response()

        # Process the response: consultarAlertas
        if response.ok:
            logger.info("POST request successful.")
            logger.info(f"Response Data: {response.text}")
        else:
            logger.error(f"POST request failed with status code {response.status_code}")

        return response

    def list_noti_men_pag(self):
        # Make a GET request : listNotiMenPag
        POST_URL = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/listNotiMenPag?tipoMsj=2&codCarpeta=00&codEtiqueta=&page=1&des_asunto=&codMensaje=&tipoOrden=NADA&_=1732302915482"
        POST_DATA = {
            "tipoMsj":"2",
            "codCarpeta":"00",
            "codEtiqueta": "",
            "page":"1",
            "des_asunto":"",
            "codMensaje":"",
            "tipoOrden":"NADA",
            "_":"1732302915482"
        }
        ADDITIONAL_HEADERS = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-language": "en-US,en;q=0.9,es;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "ww1.sunat.gob.pe",
            "Referer": "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/master?hc=9800d69758bbdd9790a73f5c400fca03efed21f8&token=rO0ABXNyAC1wZS5nb2Iuc3VuYXQudGVjbm9sb2dpYS5tZW51LmJlYW4uVXN1YXJpb0JlYW6pwYmu%2FJtYOAIAFFMAB25pdmVsVU9MAAphcGVNYXRlcm5vdAASTGphdmEvbGFuZy9TdHJpbmc7TAAKYXBlUGF0ZXJub3EAfgABTAAHY29kQ2F0ZXEAfgABTAAJY29kRGVwZW5kcQB%2BAAFMAAxjb2RUT3BlQ29tZXJxAH4AAUwABWNvZFVPcQB%2BAAFMAAZjb3JyZW9xAH4AAUwAB2Rlc0NhdGVxAH4AAUwABWRlc1VPcQB%2BAAFMAAJpZHEAfgABTAAJaWRDZWx1bGFycQB%2BAAFMAAVsb2dpbnEAfgABTAADbWFwdAAPTGphdmEvdXRpbC9NYXA7TAAObm9tYnJlQ29tcGxldG9xAH4AAUwAB25vbWJyZXNxAH4AAUwAC25yb1JlZ2lzdHJvcQB%2BAAFMAAZudW1SVUNxAH4AAUwABnRpY2tldHEAfgABTAAKdXN1YXJpb1NPTHEAfgABeHAAAHQAAHQAAHQAAHQABDAwMjN0AAB0AAB0AAB0AAB0AAB0AAB0AAEtdAATMjA2MDYyMDg0MTRBTExPREFOU3NyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAAKdAAHZGRwRGF0YXNxAH4AED9AAAAAAAAMdwgAAAAQAAAACXQACXQxMjM4X2VtcHQAATB0AApkZHBfZXN0YWRvdAACMDB0AApkZHBfdHBvZW1wdAACMzl0AApkZHBfZmxhZzIydAACMDB0AApkZHBfbnVtcmVndAAEMDAyM3QACmRkcF91YmlnZW90AAYxNTAxMzV0AApkZHBfdGFtYW5vdAACMDN0AAhkZHBfY2lpdXQABTc0MTQ1dAAKZGRwX251bXJ1Y3QACzIwNjA2MjA4NDE0eHQACXRpcE9yaWdlbnQAAklUdAAFcm9sZXNzcQB%2BABA%2FQAAAAAAAEHcIAAAAEAAAAAB4dAAKdGlwVXN1YXJpb3QAATB0AAZpZE1lbnV0AA0xMzI3MTQxNDUxOTk0dAAIam5kaVBvb2x0AAVwMDAyM3QADnZpZ0ludm9jYUhhc3Rhc3IADmphdmEubGFuZy5Mb25nO4vkkMyPI98CAAFKAAV2YWx1ZXhyABBqYXZhLmxhbmcuTnVtYmVyhqyVHQuU4IsCAAB4cAAAAZNVVhv4dAAOdmlnSW52b2NhRGVzZGVzcQB%2BADEAAAGTVUwJ2HQABmlzQ2xvbnNyABFqYXZhLmxhbmcuQm9vbGVhbs0gcoDVnPruAgABWgAFdmFsdWV4cAB0AAxwcmltZXJBY2Nlc29zcQB%2BADcBeHQAEU1FUktJIFBFUlUgUy5BLkMudAARTUVSS0kgUEVSVSBTLkEuQy50AAB0AAsyMDYwNjIwODQxNHQAEzEzMjcxNDE0NTE5OTQtYnV6b250AAhBTExPREFOUw%3D%3D",
            "Sec-Ch-Ua": 'Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Ruc": "20606208414"
            
        }
        response = session.make_get_request(url=POST_URL, data=POST_DATA, headers=ADDITIONAL_HEADERS)      

        # Process the response: consultarAlertas
        if response.ok:
            logger.info("POST request successful.")
            logger.info(f"Response Data: {response.text}")
        else:
            logger.error(f"POST request failed with status code {response.status_code}")

        return response

    def close_extraction(self):
        x_bottom_salir = self.config["XPATHS"]["x_bottom_logout"]
        workflow = [
            {"action": "click", "by": By.XPATH, "value": x_bottom_salir, "delay": 6},
        ]
        self.automator.execute_workflow(self.config["WEBSITE"]["url_start"], workflow)


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
