from langchain.chains import (create_extraction_chain,
                              create_extraction_chain_pydantic)
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from selenium.webdriver.common.by import By

from application.extract_notification_base import ExtractNotificationBase
import os

class ExtractNotificationLLM(ExtractNotificationBase):
    def __init__(self):
        super().__init__()
        self.notification_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "listaMensajes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "description": "Unique identifier for the message."
                            },
                            "subject": {
                                "type": "string",
                                "description": "Subject of the message."
                            },
                            "publish_date": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Publish date and time of the message."
                            },
                            "type": {
                                "type": "string",
                                "description": "Type of the message (e.g., 'RESOLUCIONES DE COBRANZA', 'RESOLUCIONES DE FRACCIONAMIENTO', 'VALORES')."
                            },
                            "url_attachment": {
                                "type": "string",
                                "format": "uri",
                                "description": "URL of the attachment, if any."
                            }
                        },
                        "required": ["id", "subject", "publish_date", "type"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["listaMensajes"],
            "additionalProperties": False
            }

        openai_api_key = os.getenv('OPENAI_API_KEY')

        self.llm = ChatOpenAI(temperature=0, model="gpt-4o-mini",
                        openai_api_key=openai_api_key)

    def extract(self, session):
        session.automator.driver.switch_to.frame(session.automator.driver.find_element(By.NAME, "iframeApplication"))

        notification_elements = session.automator.get_element(By.XPATH, '//ul[@id="listaMensajes"]').get_attribute("outerHTML")
        results = create_extraction_chain(schema=self.notification_schema, llm=self.llm).run(notification_elements)

        session.automator.driver.switch_to.default_content()

        return results[0]['listaMensajes']
