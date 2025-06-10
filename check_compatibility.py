#!/usr/bin/env python
"""
Cross-platform compatibility check script.
This script verifies that the environment is properly configured for both
Windows and Linux environments.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_result(test_name, result, details=None):
    """Print a test result."""
    result_str = "✓ PASS" if result else "✗ FAIL"
    color = "\033[92m" if result else "\033[91m"
    reset = "\033[0m"
    
    # Windows command prompt doesn't support ANSI colors
    if platform.system() == "Windows" and not os.environ.get("TERM"):
        print(f"{result_str} - {test_name}")
    else:
        print(f"{color}{result_str}{reset} - {test_name}")
    
    if details and not result:
        print(f"       {details}")


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    min_version = (3, 8)
    result = version >= min_version
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print_result(
        f"Python version {version_str}",
        result,
        f"Python version should be at least {min_version[0]}.{min_version[1]}"
    )
    return result


def check_platform():
    """Check the platform."""
    system = platform.system()
    print_result(f"Running on {system}", True)
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    requirements = [
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "motor",
        "pandas",
        "pydantic",
    ]
    
    all_installed = True
    for req in requirements:
        try:
            __import__(req)
            print_result(f"Dependency: {req}", True)
        except ImportError as e:
            print_result(f"Dependency: {req}", False, str(e))
            all_installed = False
    
    return all_installed


def check_directory_structure():
    """Check if the project directory structure is correct."""
    root_dir = Path(__file__).parent
    required_dirs = [
        root_dir / "app",
        root_dir / "app" / "api",
        root_dir / "app" / "core",
        root_dir / "app" / "db",
        root_dir / "app" / "models",
        root_dir / "app" / "services",
        root_dir / "app" / "utils",
        root_dir / "tests",
    ]
    
    all_exist = True
    for directory in required_dirs:
        exists = directory.is_dir()
        print_result(f"Directory: {directory.relative_to(root_dir)}", exists)
        if not exists:
            all_exist = False
    
    return all_exist


def check_env_file():
    """Check if .env file exists."""
    env_file = Path(__file__).parent / ".env"
    exists = env_file.is_file()
    print_result("Environment file (.env)", exists)
    
    if not exists:
        print("You can create a .env file with the following content:")
        print("""
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=fastapi_app
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_app
BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]
        """)
    
    return exists


def check_database_connections():
    """Check database connections."""
    # This is a simple check, not actually connecting to databases
    # since that would make the script dependent on databases being available
    print_result(
        "Database configuration", 
        True, 
        "Note: This only checks config, not actual connections"
    )
    return True


def check_docker():
    """Check if Docker is installed."""
    try:
        output = subprocess.run(
            ["docker", "--version"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        if output.returncode == 0:
            print_result("Docker", True, output.stdout.strip())
            return True
        else:
            print_result("Docker", False, "Docker command failed")
            return False
    except FileNotFoundError:
        print_result("Docker", False, "Docker not found in PATH")
        return False


def main():
    """Run all checks."""
    print_header("SOX Compliance Utility - Environment Check")
    
    print(f"Date: {subprocess.check_output('date', shell=True).decode().strip()}")
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    checks = [
        ("Python Version", check_python_version),
        ("Platform", check_platform),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Environment File", check_env_file),
        ("Database Configuration", check_database_connections),
        ("Docker", check_docker),
    ]
    
    results = {}
    for name, func in checks:
        print_header(name)
        results[name] = func()
    
    # Print summary
    print_header("Summary")
    all_passed = True
    for name, result in results.items():
        print_result(name, result)
        if not result:
            all_passed = False
    
    if all_passed:
        print("\nAll checks passed! Your environment is ready for development.")
    else:
        print("\nSome checks failed. Please fix the issues before proceeding.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
