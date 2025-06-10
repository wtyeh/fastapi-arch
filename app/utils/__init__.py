"""
Utility modules package.
"""
from app.utils.data_dir import (
    ensure_directories,
    get_app_data_dirs,
    get_project_data_dir,
    get_system_data_dir,
)
from app.utils.data_processing import (
    filter_dataframe,
    group_and_aggregate,
    merge_dataframes,
    process_dataframe,
    read_csv_file,
    save_csv_file,
)
from app.utils.platform import (
    get_app_dir,
    get_data_dir,
    get_db_path,
    get_platform_name,
    get_temp_dir,
    is_linux,
    is_macos,
    is_windows,
)
from app.utils.security import get_password_hash, verify_password

__all__ = [
    # Data processing
    "process_dataframe",
    "merge_dataframes",
    "filter_dataframe",
    "group_and_aggregate",
    "read_csv_file",
    "save_csv_file",
    
    # Platform utilities
    "get_platform_name",
    "is_windows",
    "is_linux",
    "is_macos",
    "get_app_dir",
    "get_data_dir",
    "get_temp_dir",
    "get_db_path",
    
    # Data directories
    "get_system_data_dir",
    "get_project_data_dir",
    "ensure_directories",
    "get_app_data_dirs",
    
    # Security
    "get_password_hash",
    "verify_password",
]