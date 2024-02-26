import pandas as pd
import re

def check_non_numerical_date(df: pd.DataFrame, columns_list: list, intended_type: str):
    """function to check if specific columns have non_numerical or non_date values

    Args:
        df (pd.DataFrame): the dataframe
        columns_list (list): list of columns to apply the function on
        intended_type (str): the intended type to verify for (numerical or date)
    """
    
    if intended_type == "numerical":
        for column in columns_list:
            non_numerical_values = df.loc[~df[column].apply(pd.to_numeric, errors='coerce').notna()]
            print("The non_numerical_values in column {} : ".format(column), non_numerical_values[column])

    elif intended_type == "date":
        for column in columns_list:
            non_numerical_values = df.loc[~df[column].apply(pd.to_datetime, errors='coerce').notna()]
            print("The non_date_values in column {} : ".format(column), non_numerical_values[column])
            
# convert to numerical
def convert_to_numerical(df: pd.DataFrame, columns_list: list):
    """function to convert specific column into type numeric

    Args:
        df (pd.DataFrame): the dataframe
        columns_list (list): list of columns to apply the function on

    Returns:
        pd.DataFrame: the updated DataFrame
    """
    
    for column in columns_list:
        df[column] = df[column].apply(pd.to_numeric)
    
    return df
        
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

