from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.database import Base


class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(String, unique=True, nullable=False)

    original_filename = Column(String, nullable=False)

    stored_filename = Column(String, nullable=False)

    extension = Column(String, nullable=False)

    file_size_mb = Column(Float, nullable=False)

    upload_time = Column(DateTime, nullable=False)

    status = Column(String, nullable=False)