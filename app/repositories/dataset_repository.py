from sqlalchemy.orm import Session

from app.models.dataset import Dataset


class DatasetRepository:

    @staticmethod
    def create(db: Session, dataset: Dataset):

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return dataset