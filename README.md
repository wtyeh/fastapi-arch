# SOX Compliance Utility

This project is a FastAPI application that follows clean architecture principles and connects to both MongoDB and PostgreSQL databases. It's designed to work seamlessly on both Windows and Linux environments.

> **Note**: This README consolidates information previously spread across multiple platform-specific files (README.md, README_WINDOWS.md, README_LINUX.md) into a single, comprehensive guide.

## Features

- **FastAPI** for REST API endpoints
- **SQLModel** for PostgreSQL ORM (combining SQLAlchemy core with Pydantic models)
- **Motor** for MongoDB async operations
- **Pandas** for data processing and transformation
- **Cross-platform compatibility** with Windows and Linux support
- Clean, layered architecture with:
  - API layer (routes/endpoints)
  - Service layer (business logic)
  - Repository layer (data access)
  - Domain layer (models/schemas)
  - Utility modules

## Architecture

The project follows a clean architecture approach with the following layers:

- **API Layer**: Handles HTTP requests and responses
- **Service Layer**: Contains business logic
- **Repository Layer**: Handles data access
- **Domain Layer**: Contains domain models and business entities
- **Utility Layer**: Contains utility functions and helpers

## Project Structure

```
app/
├── api/
│   └── routes/
│       ├── __init__.py
│       ├── users.py
│       └── logs.py
├── core/
│   ├── __init__.py
│   └── config.py
├── db/
│   ├── __init__.py
│   ├── mongodb.py
│   ├── postgres.py
│   └── repositories/
│       ├── __init__.py
│       ├── base.py
│       ├── mongodb.py
│       ├── user.py
│       └── log_entry.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── document.py
│   └── user.py
├── services/
│   ├── __init__.py
│   ├── user.py
│   └── log_entry.py
├── utils/
│   ├── __init__.py
│   ├── data_dir.py
│   ├── data_processing.py
│   ├── platform.py
│   └── security.py
└── main.py
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Docker and Docker Compose (optional, for containerized setup)
- PostgreSQL (optional, if not using Docker)
- MongoDB (optional, if not using Docker)

### Installation

#### Automated Setup (Recommended)

Choose the appropriate setup script for your platform:

**Windows:**
```batch
setup.bat
```

**Linux/Mac:**
```bash
# Make the script executable
chmod +x setup.sh
# Run the setup script
./setup.sh
```

**Cross-platform Python Script:**
```bash
python setup_project.py
```

#### Manual Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   # All platforms
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```bash
   # Windows
   .\.venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   # For development (includes all dependencies)
   pip install -r requirements-dev.txt
   
   # Alternatively, use pip's editable install with dev extras
   pip install -e ".[dev]"
   ```

5. Create a `.env` file in the project root with the following content:
   ```
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=fastapi_app
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=fastapi_app
   BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]
   ```

### Running the Application

Several methods are available to run the application:

#### Using Command Line

```bash
# All platforms
python -m uvicorn app.main:app --reload
```

#### Using the Run Script

```bash
# All platforms
python run.py
```

#### Using VS Code Tasks

1. Open the project in VS Code
2. Press `Ctrl+Shift+B` or select "Run Build Task..."
3. Choose "Run FastAPI Server"

#### Using Make (Linux/Mac or Windows with Make installed)

```bash
make run
```

#### Using Docker

```bash
# Build and start containers
docker-compose up -d

# Stop containers
docker-compose down
```

### API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests

```bash
# Using pytest directly
pytest

# Using VS Code task
# Press Ctrl+Shift+B and select "Run Tests"
```

### Running Tests with Coverage

```bash
# Using pytest directly
pytest --cov=app --cov-report=term --cov-report=html

# Using VS Code task
# Press Ctrl+Shift+B and select "Run Tests with Coverage"
```

### Code Formatting

```bash
# Using formatting tools directly
black .
isort .

# Using VS Code task
# Press Ctrl+Shift+B and select "Format Code"
```

### Linting

```bash
# Using linting tool directly
flake8

# Using VS Code task
# Press Ctrl+Shift+B and select "Lint Code"
```

### Pre-commit Hooks

Install pre-commit hooks to automate checks before each commit:

```bash
pre-commit install
```

## Cross-Platform Compatibility

This project has been designed to work seamlessly on both Windows and Linux environments.

### Cross-Platform Features

1. **Path handling**: Uses `pathlib.Path` for platform-independent path operations
2. **Setup scripts**: Dedicated setup scripts for different platforms
3. **Database connections**: Platform-agnostic database connection handling
4. **Environment configurations**: Consistent environment variable handling
5. **Development tools**: VS Code tasks and settings for cross-platform development

### Compatibility Check

Run the compatibility check script to verify your environment:

```bash
python check_compatibility.py
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Check if PostgreSQL/MongoDB services are running
- Verify connection strings in `.env` file
- Check firewall settings

#### Python Environment Issues
- Ensure Python 3.11+ is installed and in PATH
- Check virtual environment activation
- Verify pip is updated: `pip install --upgrade pip`

#### Permission Issues
- **Windows**: Run as Administrator when needed
- **Linux**: Use sudo for system-level operations

#### Docker Issues
- Ensure Docker service is running
- Check Docker logs: `docker-compose logs`

### Platform-Specific Troubleshooting

#### Windows
- **Path issues**: 
  - Windows has a 260-character path limit; use shorter paths or enable long paths
  - Use `\\` or raw strings `r"C:\path"` in Python code when handling paths
- **Line endings**: Set Git to handle line endings consistently with `git config --global core.autocrlf input`
- **Python in PATH**: Ensure "Add Python to PATH" was checked during installation
- **Package installation**: If you encounter issues, try `pip install --no-cache-dir -r requirements.txt`

#### Linux
- **Dependencies**: You might need to install development packages:
  ```bash
  # Ubuntu/Debian
  sudo apt install python3-dev build-essential libpq-dev
  
  # CentOS/RHEL
  sudo dnf install python3-devel postgresql-devel
  
  # Arch Linux
  sudo pacman -S base-devel postgresql-libs
  ```
- **File permissions**: Ensure correct permissions with `chmod +x *.sh`
- **Service management**: Check service status with `systemctl status postgresql mongodb`
- **Port conflicts**: Check if ports are in use with `ss -tuln | grep 8000`

For additional help, run the compatibility check script:

```bash
python check_compatibility.py
```

## License

This project is licensed under the MIT License.

---

> **Note on deprecated files**: The platform-specific README files (`README_WINDOWS.md` and `README_LINUX.md`) have been consolidated into this main README. They are kept for reference but may contain outdated information.
# fastapi-arch
