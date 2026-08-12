import pandas as pd


class ValidationService:

    @staticmethod
    def validate_dataset(df):

        errors = []
        warnings = []

        if df.empty:
            errors.append("Dataset is empty.")

        if len(df.columns) == 0:
            errors.append("Dataset contains no columns.")

        if df.isnull().sum().sum() > 0:
            warnings.append("Dataset contains missing values.")

        duplicate_count = int(df.duplicated().sum())

        if duplicate_count > 0:
            warnings.append(
                f"Dataset contains {duplicate_count} duplicate rows."
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    @staticmethod
    def check_negative_values(df):

        warnings = []

        for column in df.columns:

            if not pd.api.types.is_numeric_dtype(df[column]):
                continue

            negative_count = (df[column] < 0).sum()

            if negative_count > 0:
                warnings.append(
                    f"Column '{column}' contains "
                    f"{negative_count} negative values."
                )

        return warnings