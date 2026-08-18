from sqlalchemy.orm import Session

from app.models.pipeline import Pipeline


class PipelineRepository:

    @staticmethod
    def create(db: Session, pipeline: Pipeline):

        db.add(pipeline)
        db.commit()
        db.refresh(pipeline)

        return pipeline

    @staticmethod
    def get_by_id(db: Session, pipeline_id: str):

        return db.query(Pipeline).filter(
            Pipeline.pipeline_id == pipeline_id
        ).first()

    @staticmethod
    def get_all(db: Session):

        return db.query(Pipeline).all()