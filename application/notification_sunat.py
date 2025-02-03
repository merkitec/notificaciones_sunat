import json
import os
import pandas as pd

from application.save_notification_base import SaveNotificationBase
from infrastructure.extract_notification_manual import ExtractNotificationManual
from application.http_session_rpa import HttpSessionRpa

class NotificationSunat():
    def __init__(self, extractor: ExtractNotificationManual, 
                 session: HttpSessionRpa,
                 persist: SaveNotificationBase):
        self.extractor = extractor
        self.session = session
        self.persist = persist
    
    def process_notification(self, companies):
        for idx, credencial in companies.iterrows():
            self.session.open_mailbox(credencial)
            notifications = self.extractor.extract(self.session)
            self.session.close_extraction()

            self.persist.save(notifications, credencial['RUC'])

        self.session.close()
