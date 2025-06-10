"""
Data processing utilities module.
"""
import os
from pathlib import Path
from typing import Optional, Union

import pandas as pd


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process pandas DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: Processed DataFrame
    """
    # Example processing logic
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.fillna(0)
    
    # Convert data types
    # df['column'] = df['column'].astype(int)
    
    return df


def read_csv_file(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """
    Read CSV file with platform-independent path handling.
    
    Args:
        file_path (Union[str, Path]): Path to CSV file
        **kwargs: Additional arguments for pd.read_csv
        
    Returns:
        pd.DataFrame: DataFrame from CSV
    """
    # Convert string path to Path object for cross-platform compatibility
    path = Path(file_path) if isinstance(file_path, str) else file_path
    return pd.read_csv(path, **kwargs)


def save_csv_file(df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
    """
    Save DataFrame to CSV with platform-independent path handling.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        file_path (Union[str, Path]): Path to save CSV file
        **kwargs: Additional arguments for df.to_csv
    """
    # Convert string path to Path object for cross-platform compatibility
    path = Path(file_path) if isinstance(file_path, str) else file_path
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, **kwargs)


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str) -> pd.DataFrame:
    """
    Merge two DataFrames.
    
    Args:
        df1 (pd.DataFrame): First DataFrame
        df2 (pd.DataFrame): Second DataFrame
        on (str): Column to merge on
        
    Returns:
        pd.DataFrame: Merged DataFrame
    """
    return pd.merge(df1, df2, on=on)


def filter_dataframe(df: pd.DataFrame, column: str, value: any) -> pd.DataFrame:
    """
    Filter DataFrame by column value.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        column (str): Column to filter on
        value (any): Value to filter for
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    return df[df[column] == value]


def group_and_aggregate(df: pd.DataFrame, group_by: str, agg_column: str, agg_func: str) -> pd.DataFrame:
    """
    Group and aggregate DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        group_by (str): Column to group by
        agg_column (str): Column to aggregate
        agg_func (str): Aggregation function
        
    Returns:
        pd.DataFrame: Aggregated DataFrame
    """
    return df.groupby(group_by)[agg_column].agg(agg_func).reset_index()
