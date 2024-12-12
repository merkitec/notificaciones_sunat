from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import logging
import os

from infrastructure.selenium_rpa import SeleniumRpa
from application.http_session_rpa import HttpSessionRpa
from application.extract_notification_base import ExtractNotificationBase

logger = logging.getLogger(__name__)

class ExtractNotificationManual(ExtractNotificationBase):
    def __init__(self):
        pass

    def extract(self, session:HttpSessionRpa):
        notification_data = []        
        session.automator.driver.switch_to.frame(session.automator.driver.find_element(By.NAME, "iframeApplication"))

        notification_elements = session.automator.get_all_elements(By.XPATH, '//ul[@id="listaMensajes"]/li')
 
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