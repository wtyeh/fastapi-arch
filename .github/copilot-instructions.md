<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Project Instructions

This is a FastAPI project following clean architecture principles with:

1. FastAPI as the web framework
2. Connections to both MongoDB and PostgreSQL databases
3. Clean, layered architecture with:
   - API layer (routes/endpoints)
   - Service layer (business logic)
   - Repository layer (data access)
   - Domain layer (models/schemas)
   - Utility modules

4. Technical requirements:
   - FastAPI for REST API endpoints
   - Pydantic for data validation and settings management
   - SQLModel for PostgreSQL ORM (combining SQLAlchemy core with Pydantic models)
   - Motor for MongoDB async operations
   - Pandas for data processing and transformation
   - Dependency injection for service components
   - Environment-based configuration

5. Best engineering practices:
   - Unit tests with pytest (minimum 80% coverage)
   - Integration tests for API endpoints
   - Type hints throughout the codebase
   - Documentation with docstrings
   - Linting with flake8/black/isort
   - Pre-commit hooks
   - CI/CD pipeline configuration
