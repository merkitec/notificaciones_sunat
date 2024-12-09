from abc import ABC, abstractmethod

from application.http_session_rpa import HttpSessionRpa

class ExtractNotificationBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def extract(self, session:HttpSessionRpa):
        pass