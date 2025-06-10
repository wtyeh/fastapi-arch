#!/bin/bash
# Linux/Mac setup script for SOX Compliance Utility

# Print colored text
print_colored() {
  local color=$1
  local text=$2
  
  case $color in
    "red") echo -e "\033[91m$text\033[0m" ;;
    "green") echo -e "\033[92m$text\033[0m" ;;
    "yellow") echo -e "\033[93m$text\033[0m" ;;
    "blue") echo -e "\033[94m$text\033[0m" ;;
    *) echo "$text" ;;
  esac
}

print_colored "green" "===== SOX Compliance Utility Setup (Linux/Mac) ====="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
  print_colored "red" "Python 3 is not installed or not in PATH"
  print_colored "red" "Please install Python 3.8 or higher and try again"
  exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
print_colored "blue" "Python version: $python_version"

# Setup virtual environment
if [ ! -d ".venv" ]; then
  print_colored "blue" "Creating virtual environment..."
  python3 -m venv .venv
  if [ $? -ne 0 ]; then
    print_colored "red" "Failed to create virtual environment"
    exit 1
  fi
else
  echo "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo
print_colored "blue" "Installing dependencies..."
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
if [ $? -ne 0 ]; then
  print_colored "red" "Failed to install dependencies"
  exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
  print_colored "blue" "Creating .env file..."
  cat > .env << EOF
# Environment variables for SOX Compliance Utility
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=fastapi_app
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_app
BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]
EOF
  echo ".env file created"
else
  echo ".env file already exists"
fi

echo
print_colored "green" "===== Setup completed successfully! ====="
echo
print_colored "yellow" "Next steps:"
echo "1. The virtual environment is already activated"
echo "2. Start the application: python -m uvicorn app.main:app --reload"
echo "   or use: make run"
echo "3. Visit http://localhost:8000/docs to see the API documentation"
echo
