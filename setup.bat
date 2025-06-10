@echo off
:: Windows setup script for SOX Compliance Utility
echo ===== SOX Compliance Utility Setup (Windows) =====
echo.

:: Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    exit /b 1
)

:: Setup virtual environment
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment
        exit /b 1
    )
) else (
    echo Virtual environment already exists
)

:: Activate virtual environment and install dependencies
echo.
echo Installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies
    exit /b 1
)

:: Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo # Environment variables for SOX Compliance Utility
        echo MONGODB_URI=mongodb://localhost:27017
        echo MONGODB_DB_NAME=fastapi_app
        echo POSTGRES_SERVER=localhost
        echo POSTGRES_USER=postgres
        echo POSTGRES_PASSWORD=postgres
        echo POSTGRES_DB=fastapi_app
        echo BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]
    ) > .env
    echo .env file created
) else (
    echo .env file already exists
)

echo.
echo ===== Setup completed successfully! =====
echo.
echo Next steps:
echo 1. The virtual environment is already activated
echo 2. Start the application: python -m uvicorn app.main:app --reload
echo    or use: python -m uvicorn app.main:app --reload
echo 3. Visit http://localhost:8000/docs to see the API documentation
echo.
