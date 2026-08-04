import pandas as pd
from pathlib import Path


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

        return {
            "summary": summary,
            "statistics": statistics,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows
        }