from datetime import date
from pydantic import BaseModel


class DateFilter(BaseModel):
    date_from: date
    date_to: date
    channel: str | None = None
    campaign: str | None = None
    device: str | None = None
    region: str | None = None
