import json
import logging
import os
import pandas as pd

from application.estudio_contable_service import EstudioContableService
from application.save_notification_base import SaveNotificationBase
from cross_cutting.settings import Settings
from infrastructure.extract_notification_manual import ExtractNotificationManual
from application.http_session_rpa import HttpSessionRpa
logger = logging.getLogger(__name__)

class NotificationSunat():
    def __init__(self, extractor: ExtractNotificationManual, 
                 session: HttpSessionRpa,
                 persist: SaveNotificationBase,
                 estudio_contable_svc: EstudioContableService,
                 settings: Settings):
        self.extractor = extractor
        self.session = session
        self.persist = persist
        self.estudio_contable_svc = estudio_contable_svc
        self.settings = settings
    
    def process_notification(self):
        companies = self.estudio_contable_svc.get_rucs_by_estudio_contable(self.settings.ESTUDIO_CONTABLE_RUC)

        for credencial in companies:
            logger.info(f"Credencial RUC: {credencial["RUC"]}")
            self.session.open_mailbox(credencial)
            notifications = self.extractor.extract(self.session, 
                                                   { "estudio_contable_ruc": self.settings.ESTUDIO_CONTABLE_RUC,
                                                     "ruc": credencial["RUC"] })
            self.session.close_extraction()
            
            self.persist.save(notifications, credencial['RUC'])


        self.session.close()
