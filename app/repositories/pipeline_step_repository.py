from sqlalchemy.orm import Session

from app.models.pipeline_step import PipelineStep


class PipelineStepRepository:

    @staticmethod
    def create(db: Session, step: PipelineStep):

        db.add(step)
        db.commit()
        db.refresh(step)

        return step

    @staticmethod
    def get_by_pipeline_id(
        db: Session,
        pipeline_id: str
    ):

        return db.query(PipelineStep).filter(
            PipelineStep.pipeline_id == pipeline_id
        ).order_by(
            PipelineStep.step_order
        ).all()