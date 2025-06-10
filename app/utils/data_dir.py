"""
Data directory handling module.
"""
import os
import platform
import sys
from pathlib import Path
from typing import Dict, Optional


def get_system_data_dir() -> Path:
    """
    Get the system-specific data directory path.
    
    Returns:
        Path: System data directory path
    """
    system = platform.system()
    
    if system == "Windows":
        # On Windows, use AppData/Local
        app_data = os.environ.get("LOCALAPPDATA")
        if app_data:
            return Path(app_data) / "SOXComplianceUtility"
        return Path.home() / "AppData" / "Local" / "SOXComplianceUtility"
    
    elif system == "Darwin":  # macOS
        # On macOS, use ~/Library/Application Support
        return Path.home() / "Library" / "Application Support" / "SOXComplianceUtility"
    
    else:  # Linux and others
        # On Linux, use ~/.local/share
        xdg_data_home = os.environ.get("XDG_DATA_HOME")
        if xdg_data_home:
            return Path(xdg_data_home) / "sox-compliance-utility"
        return Path.home() / ".local" / "share" / "sox-compliance-utility"


def get_project_data_dir() -> Path:
    """
    Get the project data directory path.
    
    Returns:
        Path: Project data directory path
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Create a data directory in the project root
    data_dir = project_root / "data"
    return data_dir


def ensure_directories(base_dir: Path) -> Dict[str, Path]:
    """
    Ensure that all required directories exist.
    
    Args:
        base_dir (Path): Base directory path
        
    Returns:
        Dict[str, Path]: Dictionary of directory paths
    """
    # Create base directory if it doesn't exist
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    dirs = {
        "logs": base_dir / "logs",
        "db": base_dir / "db",
        "uploads": base_dir / "uploads",
        "exports": base_dir / "exports",
        "temp": base_dir / "temp",
    }
    
    # Create each directory
    for dir_path in dirs.values():
        dir_path.mkdir(exist_ok=True)
    
    return dirs


def get_app_data_dirs(use_system_dirs: bool = False) -> Dict[str, Path]:
    """
    Get all application data directories.
    
    Args:
        use_system_dirs (bool): Whether to use system directories
        
    Returns:
        Dict[str, Path]: Dictionary of directory paths
    """
    # Determine base directory
    if use_system_dirs:
        base_dir = get_system_data_dir()
    else:
        base_dir = get_project_data_dir()
    
    # Ensure directories exist and return them
    return ensure_directories(base_dir)
