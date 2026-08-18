from app.core.config import settings
from pathlib import Path


class TransformationService:

    @staticmethod
    def transform_dataset(
        df,
        rename_columns=None,
        drop_columns=None,
        select_columns=None,
        filter_condition=None,
        sort_column=None,
        sort_ascending=True
    ):

        operations = []

        if rename_columns:
            df = TransformationService.rename_columns(
                df,
                rename_columns
            )
            operations.append("rename_columns")

        if drop_columns:
            df = TransformationService.drop_columns(
                df,
                drop_columns
            )
            operations.append("drop_columns")

        if select_columns:
            df = TransformationService.select_columns(
                df,
                select_columns
            )
            operations.append("select_columns")

        if filter_condition:
            df = TransformationService.filter_rows(
                df,
                filter_condition
            )
            operations.append("filter_rows")

        if sort_column:
            df = TransformationService.sort_rows(
                df,
                sort_column,
                sort_ascending
            )
            operations.append("sort_rows")

        transformation_info = {
            "operations_applied": operations,
            "rows": len(df),
            "columns": list(df.columns)
        }

        return df, transformation_info

    @staticmethod
    def rename_columns(df, column_mapping):

        return df.rename(columns=column_mapping)

    @staticmethod
    def drop_columns(df, columns):

        return df.drop(columns=columns)

    @staticmethod
    def select_columns(df, columns):

        return df[columns]

    @staticmethod
    def filter_rows(df, condition):

        return df.query(condition)

    @staticmethod
    def sort_rows(df, column, ascending=True):

        return df.sort_values(
            by=column,
            ascending=ascending
        )

    @staticmethod
    def save_transformed_dataset(df, filename):

        output_path = Path(settings.OUTPUT_DIR) / f"transformed_{filename}"

        df.to_csv(
            output_path,
            index=False
        )

        return output_path