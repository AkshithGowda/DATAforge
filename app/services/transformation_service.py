import pandas as pd
from pathlib import Path

from app.core.config import settings


class TransformationService:

    @staticmethod
    def rename_columns(df, column_mapping):
        df = df.rename(columns=column_mapping)
        return df

    @staticmethod
    def drop_columns(df, columns):
        df = df.drop(columns=columns)
        return df

    @staticmethod
    def select_columns(df, columns):
        df = df[columns]
        return df

    @staticmethod
    def filter_rows(df, condition):
        df = df.query(condition)
        return df

    @staticmethod
    def sort_rows(df, column, ascending=True):
        df = df.sort_values(
            by=column,
            ascending=ascending
        )
        return df

    
    
    @staticmethod
    def save_transformed_dataset(df, original_filename):

        filename = f"{original_filename}_transformed.csv"

        file_path = Path(settings.CLEANED_DIR) / filename

        df.to_csv(file_path, index=False)

        return file_path