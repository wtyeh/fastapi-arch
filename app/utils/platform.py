"""
Platform-specific utility functions.
"""
import os
import platform
import sys
from pathlib import Path
from typing import Optional


def get_platform_name() -> str:
    """
    Get the current platform name.
    
    Returns:
        str: Platform name ('windows', 'linux', 'darwin', etc.)
    """
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    return system


def is_windows() -> bool:
    """
    Check if the current platform is Windows.
    
    Returns:
        bool: True if Windows, False otherwise
    """
    return get_platform_name() == 'windows'


def is_linux() -> bool:
    """
    Check if the current platform is Linux.
    
    Returns:
        bool: True if Linux, False otherwise
    """
    return get_platform_name() == 'linux'


def is_macos() -> bool:
    """
    Check if the current platform is macOS.
    
    Returns:
        bool: True if macOS, False otherwise
    """
    return get_platform_name() == 'macos'


def get_app_dir() -> Path:
    """
    Get the application directory path.
    
    Returns:
        Path: Application directory path
    """
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """
    Get the data directory path.
    Creates the directory if it doesn't exist.
    
    Returns:
        Path: Data directory path
    """
    # Create a data directory in the application directory
    data_dir = get_app_dir() / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir


def get_temp_dir() -> Path:
    """
    Get a temporary directory path suitable for the current platform.
    Creates the directory if it doesn't exist.
    
    Returns:
        Path: Temporary directory path
    """
    # Create a temporary directory in the application directory
    temp_dir = get_app_dir() / 'temp'
    temp_dir.mkdir(exist_ok=True)
    return temp_dir


def get_db_path(db_name: str) -> Path:
    """
    Get a database file path suitable for the current platform.
    Creates the parent directory if it doesn't exist.
    
    Args:
        db_name (str): Database name
        
    Returns:
        Path: Database file path
    """
    # Create a db directory in the application directory
    db_dir = get_app_dir() / 'db_files'
    db_dir.mkdir(exist_ok=True)
    
    # Return the database file path
    return db_dir / f"{db_name}.db"
