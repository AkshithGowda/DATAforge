from sqlalchemy.orm import Session

from app.models.cleaning_history import CleaningHistory


class CleaningHistoryRepository:

    @staticmethod
    def create(db: Session, history: CleaningHistory):

        db.add(history)
        db.commit()
        db.refresh(history)

        return history
    @staticmethod
    def get_by_dataset_id(db: Session, dataset_id: str):

        return db.query(CleaningHistory).filter(
            CleaningHistory.dataset_id == dataset_id
        ).all()