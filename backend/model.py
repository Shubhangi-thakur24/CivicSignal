
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, DateTime, Text
from backend.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)
    text_original = Column(Text, nullable=False)
    language = Column(String, default="unknown")
    issue_type = Column(String, default="unknown")
    location_original = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)
    ingested_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
