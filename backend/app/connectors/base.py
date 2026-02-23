from abc import ABC, abstractmethod
from datetime import date


class BaseConnector(ABC):
    key: str
    title: str

    @abstractmethod
    def fetch(self, date_from: date, date_to: date) -> list[dict]:
        raise NotImplementedError
