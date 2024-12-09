from datetime import datetime
import json
import os
import pandas as pd

from application.extract_notification import ExtractNotification
from application.http_session_rpa import HttpSessionRpa

class NotificationSunat():
    def __init__(self, extrator: ExtractNotification, session: HttpSessionRpa):
        self.extractor = extrator
        self.session = session

    def save_results(self, file_path, notifications, id_name_part):   
        os.makedirs(file_path, exist_ok=True)
        with open(f'{file_path}/notifica_{id_name_part}_{datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}.json', 'w') as json_file:
            json.dump(notifications, json_file, indent=4)

        df = pd.DataFrame(notifications)
        df.to_excel(f"{file_path}/notifica_{id_name_part}_{datetime.now().strftime('%Y.%m.%d_%H.%M.%S')}.xlsx")

    def process_notification(self, companies):
        for idx, credencial in companies.iterrows():
            self.session.open_mailbox(credencial)
            notifications = self.extractor.extract(self.session)
            self.session.close_extraction()

            self.save_results('./results', notifications, credencial['RUC'])

        self.session.close()
