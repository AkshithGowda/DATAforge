from sqlalchemy import Column, String, Integer, DateTime

from app.database.database import Base


class Pipeline(Base):

    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_id = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)

    dataset_id = Column(String, nullable=False)

    status = Column(String, default="CREATED")

    created_at = Column(DateTime, nullable=False)