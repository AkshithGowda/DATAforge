from sqlalchemy.orm import Session

from app.models.validation_history import ValidationHistory


class ValidationHistoryRepository:

    @staticmethod
    def create(db: Session, history: ValidationHistory):

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    @staticmethod
    def get_by_dataset_id(db: Session, dataset_id: str):

        return db.query(ValidationHistory).filter(
            ValidationHistory.dataset_id == dataset_id
        ).all()