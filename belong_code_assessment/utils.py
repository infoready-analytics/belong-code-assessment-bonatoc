from pathlib import Path

import pandas as pd
import requests


def check_url(url):
    """Determine whether a URL can be reached.

    Args:
        url (str): URL to test.

    Returns:
        bool: If it could be reached or not.
    """

    response = requests.get(url)

    if response.status_code == 200:
        return True

    return False


def preprocess_df(func):
    """Decorator for preprocessing a DataFrame."""

    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)

        if isinstance(df, pd.DataFrame):
            df.columns = [col.lower() for col in df.columns]
            df["hourly_counts"] = df["hourly_counts"].astype(int)

        return df

    return wrapper


@preprocess_df
def load_dataframe(filepath):
    """Load a DataFrame from a file on disk - supports JSON, CSV and parquet.

    Args:
        filepath (str or pathlib.Path): Input filepath to load.

    Raises:
        Exception: File specified by filepath is not parquet, CSV or JSON.

    Returns:
        pd.DataFrame: DataFrame containing pedestrian records.
    """

    if Path(filepath).suffix.lower() == ".parquet":
        return pd.read_parquet(filepath)
    elif Path(filepath).suffix.lower() == ".csv":
        return pd.read_csv(filepath)
    elif Path(filepath).suffix.lower() == ".json":
        return pd.read_json(filepath)

    raise Exception(f"{filepath} must be either a parquet, CSV or JSON format.")


def save_dataframe(df, filepath, fmt="csv"):
    """Utility function for saving a DataFrame to disk. Supports either csv or parquet.

    Args:
        df (pd.DataFrame: DataFrame to save.
        filepath (pathlib.Path or str): Path to save the DataFrame to.
        fmt (str, optional): Format to save the DataFrame as. Defaults to "csv".

    Raises:
        Exception: If fmt is not csv or parquet.
    """

    if fmt.lower() == "csv":
        df.to_csv(filepath, index=False)
    elif fmt.lower() == "parquet":
        df.to_parquet(filepath)
    else:
        raise Exception(f"DataFrame can only be saved to either CSV or parquet.")


def unpack_args(fdesc):
    """Unpack a tuple with an execution task.

    Args:
        fdesc (tuple): Tuple containing a function, list of arguments, and dictionary of keyword
        arguments

    Returns:
        Output of the executed function
    """

    f, args, kwargs = fdesc

    return f(*args, **kwargs)
