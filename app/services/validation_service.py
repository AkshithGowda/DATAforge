import pandas as pd


class ValidationService:

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

        warnings.extend(
            ValidationService.check_negative_values(df)
        )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    @staticmethod
    def check_outliers(df):

        warnings = []

        for column in df.columns:

            if not pd.api.types.is_numeric_dtype(df[column]):
                continue

            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            outlier_count = (
                (df[column] < lower_bound) |
                (df[column] > upper_bound)
            ).sum()

            if outlier_count > 0:
                warnings.append(
                    f"Column '{column}' contains "
                    f"{outlier_count} potential outliers."
                )

        return warnings