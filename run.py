#!/usr/bin/env python
"""
Cross-platform launcher script for the FastAPI application.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path


def run_app():
    """Run the FastAPI application."""
    # Get the Python interpreter path
    python_exe = sys.executable
    
    # Determine the command to run
    if platform.system() == "Windows":
        cmd = [python_exe, "-m", "uvicorn", "app.main:app", "--reload"]
    else:
        cmd = [python_exe, "-m", "uvicorn", "app.main:app", "--reload"]
    
    print(f"Starting FastAPI application with: {' '.join(cmd)}")
    
    # Run the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")


if __name__ == "__main__":
    run_app()