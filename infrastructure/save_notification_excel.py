from application.save_notification_base import SaveNotificationBase
from datetime import datetime
import os
import pandas as pd

class SaveNotificationExcel(SaveNotificationBase):
    def __init__(self, config=None):
        super().__init__()
        self.config = config

    def save(self, notifications, id):   
        os.makedirs(self.config["LOCAL_STORE"]['path'], exist_ok=True)
        # with open(f'{file_path}/notifica_{id_name_part}_{datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}.json', 'w') as json_file:
        #     json.dump(notifications, json_file, indent=4)

        df = pd.DataFrame(notifications)
        df.to_excel(f"{self.config['LOCAL_STORE']['path']}/notificaciones_{id}_{datetime.now().strftime('%Y.%m.%d_%H.%M.%S')}.xlsx")

