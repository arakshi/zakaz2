from datetime import date

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DateRangeFilter(BaseModel):
    date_from: date
    date_to: date
    channel: str | None = None
    campaign: str | None = None
    device: str | None = None
    region: str | None = None
