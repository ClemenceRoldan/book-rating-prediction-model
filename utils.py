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
    for col in columns:
        df[col] = df[col].apply(lambda x: x.lower() if not pd.isna(x) else x)
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

def one_hot_encode(df: pd.DataFrame, column_name: str):
    """function to apply one hot encoding on categorical columns

    Args:
        df (pd.DataFrame): the dataframe
        column_name (str): the column to apply one-hot encoding on

    Returns:
        pd.DataFrame: the updated DataFrame
    """
    encoded_columns = pd.get_dummies(df[column_name], prefix=column_name)
    
    # Concatenate the encoded columns to the original DataFrame
    df = pd.concat([df, encoded_columns], axis=1)
    
    # Drop the original column
    df.drop(column_name, axis=1, inplace=True)
    
    return df

