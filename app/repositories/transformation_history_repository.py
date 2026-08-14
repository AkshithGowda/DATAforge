from sqlalchemy.orm import Session

from app.models.transformation_history import TransformationHistory


class TransformationHistoryRepository:

    @staticmethod
    def create(db: Session, history: TransformationHistory):

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def get_by_dataset_id(db: Session, dataset_id: str):

        return db.query(TransformationHistory).filter(
            TransformationHistory.dataset_id == dataset_id
        ).all()