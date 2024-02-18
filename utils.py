import pandas as pd
import re

def to_lower(df: pd.DataFrame, columns: list):
    """funtionc to convert text columns to lower case

    Args:
        df (pd.DataFrame): the dataframe
        columns (list): the columns to apply the function on

    Returns:
        pd.DataFrame: the updated DataFrame
    """
    df[columns] = df[columns].apply(lambda x: x.str.lower() if not pd.isna(x) else x)
    return df

def sub_text(df: pd.DataFrame, columns: list, replacements: list):
    """function to replace specific content in the text

    Args:
        df (pd.DataFrame): the dataframe
        columns (list): the columns to apply the function on
        replacements (list): list of tuples ("old value", "new value")

    Returns:
        pd.DataFrame: the updated DataFrame
    """

    for pattern, replacement in replacements:
        for col in columns:
            df[col] = df[col].apply(lambda x: re.sub(pattern, replacement, x) if not pd.isna(x) else x)

    return df

