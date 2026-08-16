from sqlalchemy import Column, String, Integer, DateTime, Boolean

from app.database.database import Base


class ValidationHistory(Base):

    __tablename__ = "validation_history"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(String, nullable=False)

    valid = Column(Boolean, nullable=False)

    error_count = Column(Integer)

    warning_count = Column(Integer)

    created_at = Column(DateTime, nullable=False)