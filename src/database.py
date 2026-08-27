import duckdb
import pandas as pd


def create_database(df: pd.DataFrame):
    """
    Create an in-memory DuckDB database
    and register the DataFrame as a table.
    """

    connection = duckdb.connect(database=":memory:")

    connection.register("sales", df)

    return connection


def execute_query(connection, query: str):
    """
    Execute a SQL query and return the result
    as a Pandas DataFrame.
    """

    result = connection.execute(query).fetchdf()

    return result