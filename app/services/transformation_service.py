import pandas as pd


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