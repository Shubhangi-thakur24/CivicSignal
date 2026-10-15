
from datetime import datetime
from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    id: str = Field(min_length=1)
    text_original: str = Field(min_length=1)
    language: str = "unknown"
    issue_type: str = "unknown"
    location_original: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    created_at: datetime | None = None


class ReportResponse(BaseModel):
    id: str
    text_original: str
    language: str
    issue_type: str
    location_original: str | None
    latitude: float | None
    longitude: float | None
    created_at: datetime | None
    ingested_at: datetime

    class Config:
        from_attributes = True
