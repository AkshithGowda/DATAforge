from sqlalchemy.orm import Session

from app.models.dataset import Dataset


class DatasetRepository:

    @staticmethod
    def create(db: Session, dataset: Dataset):

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return dataset

    @staticmethod
    def get_by_id(db: Session, dataset_id: str):

        return db.query(Dataset).filter(
            Dataset.dataset_id == dataset_id
        ).first()

        print("TRANSFORMATION DATASET ID:", request.dataset_id)

        dataset = DatasetRepository.get_by_id(
            db,
            request.dataset_id
        )

        print("FOUND DATASET:", dataset)