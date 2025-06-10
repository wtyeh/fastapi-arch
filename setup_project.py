#!/usr/bin/env python
"""
Cross-platform setup script for the SOX Compliance Utility.
This script helps set up the development environment on both Windows and Linux.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path


def print_colored(text, color="green"):
    """Print colored text."""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    
    # Windows cmd doesn't support ANSI colors by default
    if platform.system() == "Windows" and not os.environ.get("TERM"):
        print(text)
    else:
        print(f"{colors.get(color, colors['green'])}{text}{colors['reset']}")


def run_command(command, shell=True):
    """Run a shell command and return its success status."""
    try:
        print_colored(f"Running: {command}", "blue")
        subprocess.run(command, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"Error running command: {e}", "red")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print_colored("Checking dependencies...", "blue")
    
    # Check Python version
    py_version = platform.python_version()
    print(f"Python version: {py_version}")
    if tuple(map(int, py_version.split('.'))) < (3, 8):
        print_colored("Python 3.8 or higher is required", "red")
        return False
    
    # Check pip
    if not run_command(f"{sys.executable} -m pip --version", shell=True):
        print_colored("pip is not installed or not working", "red")
        return False
    
    # Check Docker if it's needed
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("Docker is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_colored("Docker is not installed. Some features may not work.", "yellow")
    
    return True


def setup_virtual_env():
    """Create and activate a virtual environment."""
    print_colored("Setting up virtual environment...", "blue")
    
    venv_dir = Path(".venv")
    if venv_dir.exists():
        print("Virtual environment already exists")
    else:
        if not run_command(f"{sys.executable} -m venv .venv"):
            print_colored("Failed to create virtual environment", "red")
            return False
    
    # Print activation instructions based on platform
    if platform.system() == "Windows":
        print_colored("\nTo activate the virtual environment, run:", "yellow")
        print(".venv\\Scripts\\activate")
    else:
        print_colored("\nTo activate the virtual environment, run:", "yellow") 
        print("source .venv/bin/activate")
    
    return True


def install_dependencies():
    """Install project dependencies."""
    print_colored("Installing dependencies...", "blue")
    
    # Install development dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements-dev.txt"):
        print_colored("Failed to install development dependencies", "red")
        return False
    
    return True


def setup_env_file():
    """Create a .env file if it doesn't exist."""
    env_file = Path(".env")
    if env_file.exists():
        print(".env file already exists")
        return True
    
    print_colored("Creating .env file...", "blue")
    with open(env_file, "w") as f:
        f.write("""# Environment variables for SOX Compliance Utility
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=fastapi_app
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_app
BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]
""")
    
    print(".env file created")
    return True


def main():
    """Main setup function."""
    print_colored("=== SOX Compliance Utility Setup ===")
    
    if not check_dependencies():
        print_colored("Please install the required dependencies and try again", "red")
        return
    
    if not setup_virtual_env():
        return
    
    if not install_dependencies():
        return
    
    if not setup_env_file():
        return
    
    print_colored("\n=== Setup completed successfully! ===", "green")
    print_colored("\nNext steps:", "blue")
    print("1. Activate the virtual environment")
    print("2. Start the application: python -m uvicorn app.main:app --reload")
    print("   or use: make run")
    print("3. Visit http://localhost:8000/docs to see the API documentation")


if __name__ == "__main__":
    main()
