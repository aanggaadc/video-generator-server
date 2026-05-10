import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.core.database import Base


class Generation(Base):
    __tablename__ = "generations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    video_type = Column(String, nullable=False)
    topic = Column(String, nullable=False)

    keywords = Column(Text)
    target_audience = Column(String)
    tone = Column(String)
    duration = Column(String)

    generated_title = Column(Text)
    generated_hook = Column(Text)
    generated_script = Column(Text)
    generated_cta = Column(Text)

    generated_storyboard = Column(JSONB)

    raw_response = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )