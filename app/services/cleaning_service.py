import pandas as pd
from pathlib import Path

from app.core.config import settings

class CleaningService:

    @staticmethod
    def remove_duplicates(df):

        original_rows = len(df)

        df = df.drop_duplicates()

        removed_rows = original_rows - len(df)

        return df, removed_rows


    @staticmethod
    def handle_missing_values(df):

        missing_before = int(df.isnull().sum().sum())

        filled_columns = []

        for column in df.columns:

            if df[column].isnull().sum() == 0:
                continue

            if pd.api.types.is_numeric_dtype(df[column]):

                df[column] = df[column].fillna(
                    df[column].median()
                )

                method = "median"

            else:

                df[column] = df[column].fillna("Unknown")

                method = "Unknown"

            filled_columns.append({
                "column": column,
                "method": method
            })

        missing_after = int(df.isnull().sum().sum())

        return df, missing_before, missing_after, filled_columns

    @staticmethod
    def convert_datetime_columns(df):

        datetime_columns = []

        for column in df.columns:

            if not pd.api.types.is_object_dtype(df[column]):
                continue

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

            valid_values = converted.notna().sum()
            original_values = df[column].notna().sum()

            if original_values > 0 and valid_values == original_values:

                df[column] = converted

                datetime_columns.append({
                    "column": column,
                    "from": "object",
                    "to": "datetime"
                })

        return df, datetime_columns

    
    @staticmethod
    def clean_dataset(df):

        original_rows = len(df)

        df, duplicates_removed = CleaningService.remove_duplicates(df)

        df, missing_before, missing_after, filled_columns = (
            CleaningService.handle_missing_values(df)
        )

        df, converted_columns = CleaningService.convert_numeric_columns(df)
        df, datetime_columns = CleaningService.convert_datetime_columns(df)


        return df, {
            "original_rows": original_rows,
            "final_rows": len(df),
            "duplicates_removed": duplicates_removed,
            "missing_values_before": missing_before,
            "missing_values_after": missing_after,
            "filled_columns": filled_columns,
            "converted_columns": converted_columns
            
        }
        
    @staticmethod
    def convert_numeric_columns(df):

        converted_columns = []

        for column in df.columns:

            if not pd.api.types.is_object_dtype(df[column]):
                continue

            cleaned = (
                df[column]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.strip()
            )

            numeric_values = pd.to_numeric(
                cleaned,
                errors="coerce"
            )

            valid_values = numeric_values.notna().sum()
            original_values = df[column].notna().sum()

            if original_values > 0 and valid_values == original_values:

                df[column] = numeric_values

                converted_columns.append({
                    "column": column,
                    "from": "object",
                    "to": "numeric"
                })

        return df, converted_columns

    

    @staticmethod
    def save_cleaned_dataset(df, original_filename):

            filename = Path(original_filename).stem + "_cleaned.csv"

            file_path = Path(settings.CLEANED_DIR) / filename

            df.to_csv(file_path, index=False)

            return file_path