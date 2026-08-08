import pandas as pd


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

        for column in df.columns:

            if df[column].isnull().sum() == 0:
                continue

            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].median())

            else:
                df[column] = df[column].fillna("Unknown")

        missing_after = int(df.isnull().sum().sum())

        return df, missing_before, missing_after

    @staticmethod
    def clean_dataset(df):

            original_rows = len(df)

            df, duplicates_removed = CleaningService.remove_duplicates(df)

            df, missing_before, missing_after = (
                CleaningService.handle_missing_values(df)
            )

            return df, {
                "original_rows": original_rows,
                "final_rows": len(df),
                "duplicates_removed": duplicates_removed,
                "missing_values_before": missing_before,
                "missing_values_after": missing_after
            }