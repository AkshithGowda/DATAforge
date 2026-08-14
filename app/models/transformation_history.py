from sqlalchemy import Column, String, Integer, DateTime, Text

from app.database.database import Base


class TransformationHistory(Base):

    __tablename__ = "transformation_history"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(String, nullable=False)

    operation = Column(Text, nullable=False)

    input_rows = Column(Integer)

    output_rows = Column(Integer)

    created_at = Column(DateTime, nullable=False)