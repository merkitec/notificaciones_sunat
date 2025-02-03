from abc import ABC, abstractmethod

class SaveNotificationBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def save(self, notifications, ruc):
        pass