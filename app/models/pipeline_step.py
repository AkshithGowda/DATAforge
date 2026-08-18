from sqlalchemy import Column, String, Integer, DateTime

from app.database.database import Base


class PipelineStep(Base):

    __tablename__ = "pipeline_steps"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_id = Column(String, nullable=False)

    step_order = Column(Integer, nullable=False)

    operation = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    created_at = Column(DateTime, nullable=False)