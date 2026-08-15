from sqlalchemy import Column, String, Integer, DateTime

from app.database.database import Base


class CleaningHistory(Base):

    __tablename__ = "cleaning_history"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(String, nullable=False)

    original_rows = Column(Integer)

    final_rows = Column(Integer)

    duplicates_removed = Column(Integer)

    missing_values_before = Column(Integer)

    missing_values_after = Column(Integer)

    created_at = Column(DateTime, nullable=False)