import pandas as pd
import re

VALID_LABEL_PATTERN = re.compile(r'^[a-zA-Z_]+$')
VALID_ROLE_PATTERN = re.compile(r'^[a-zA-Z0-9_.\s+\-*]+$')
VARIABLES_PATTERN = re.compile(r'[a-zA-Z_]+')

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Add a virtual column to a dataframe
    :param df: The input pandas DataFrame.
    :param role: The mathematical expression to compute (e.g., 'col_one + col_two').
    :param new_column: The name of the new column to be added.
    :return: A new DataFrame with the added column, or an empty DataFrame if validation fails.
    """
    # Validate inputs
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame()

    if not all(isinstance(col, str) and VALID_LABEL_PATTERN.match(col) for col in df.columns):
        return pd.DataFrame()

    if not isinstance(new_column, str) or not VALID_LABEL_PATTERN.match(new_column):
        return pd.DataFrame()
    if not isinstance(role, str) or not VALID_ROLE_PATTERN.match(role):
        return pd.DataFrame()

    variables = VARIABLES_PATTERN.findall(role)
    if not all(var in df.columns for var in variables):
        return pd.DataFrame()

    # Perform the calculation
    try:
        new_series = df.eval(role)
        df[new_column] = new_series
        return df
    except Exception:
        return pd.DataFrame()
