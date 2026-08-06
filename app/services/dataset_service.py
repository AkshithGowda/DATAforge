import re
import pandas as pd

from pathlib import Path

from pandas.api.types import (
    is_integer_dtype,
    is_float_dtype,
    is_bool_dtype,
    is_object_dtype
)

class DatasetService:

    @staticmethod
    def read_dataset(file_path: Path, extension: str):

        if extension == ".csv":
            df = pd.read_csv(file_path)

        elif extension == ".xlsx":
            df = pd.read_excel(file_path)

        elif extension == ".json":
            df = pd.read_json(file_path)

        else:
            raise ValueError("Unsupported file format.")

        return df


    @staticmethod
    def generate_summary(df):

        rows = len(df)

        columns = len(df.columns)

        column_names = list(df.columns)
        
        memory_usage = round(
            df.memory_usage(deep=True).sum() / (1024 * 1024),
            2
        )
        data_types = {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }

        return {
            "rows": rows,
            "columns": columns,
            "column_names": column_names,
            "data_types": data_types,
            "memory_usage": memory_usage
        }


    @staticmethod
    def generate_statistics(df):

        statistics = df.describe(include="all")

        return statistics.fillna("").to_dict()


    @staticmethod
    def check_missing_values(df):
        missing_values = df.isnull().sum()

        return missing_values.to_dict() 

    @staticmethod
    def check_duplicates(df):

        return int(df.duplicated().sum())

    @staticmethod
    def analyze_dataset(file_path: Path, extension: str):

        df = DatasetService.read_dataset(file_path, extension)

        summary = DatasetService.generate_summary(df)

        statistics = DatasetService.generate_statistics(df)

        missing_values = DatasetService.check_missing_values(df)

        duplicate_rows = DatasetService.check_duplicates(df)

        schema = DatasetService.detect_schema(df)

        return {
            "summary": summary,
            "statistics": statistics,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "schema": schema
        }            
            

    @staticmethod
    def detect_schema(df):

        schema = {}

        for column in df.columns:

            if is_integer_dtype(df[column]):
                detected_type = "INTEGER"

            elif is_float_dtype(df[column]):
                detected_type = "FLOAT"

            elif is_bool_dtype(df[column]):
                detected_type = "BOOLEAN"

            elif is_object_dtype(df[column]):
                detected_type = DatasetService.infer_string_type(
                    df[column]
                )

            else:
                detected_type = "UNKNOWN"

            nullable = bool(df[column].isnull().any())
            unique_values = int(df[column].nunique())
            sample_value = None

            non_null = df[column].dropna()

            if not non_null.empty:
                sample_value = str(non_null.iloc[0])

            schema[column] = {
                "type": detected_type,
                "nullable": nullable,
                "unique_values": unique_values,
                "sample_value": sample_value
            }

        return schema


    @staticmethod
    def infer_string_type(series):

        cleaned_series = (
            series
            .dropna()
            .astype(str)
        )

        if cleaned_series.empty:
            return "STRING"

        sample = cleaned_series.iloc[0]

        if re.match(r"\d{4}-\d{2}-\d{2}$", sample):
            return "DATE"

        if re.match(r"\d{2}:\d{2}:\d{2}", sample):
            return "TIME"

        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", sample):
            return "EMAIL"

        if sample.lower() in {"true", "false", "yes", "no"}:
            return "BOOLEAN"

        if sample.isdigit():
            return "INTEGER"

        try:
            float(sample)
            return "FLOAT"
        except ValueError:
            pass

        return "STRING"