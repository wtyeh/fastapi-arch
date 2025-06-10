"""
Application configuration module.
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings class.
    
    Attributes:
        API_V1_STR (str): API version prefix
        PROJECT_NAME (str): Project name
        PROJECT_DESCRIPTION (str): Project description
        PROJECT_VERSION (str): Project version
        BACKEND_CORS_ORIGINS (List[AnyHttpUrl]): List of allowed CORS origins
        MONGODB_URI (str): MongoDB connection URI
        MONGODB_DB_NAME (str): MongoDB database name
        POSTGRES_SERVER (str): PostgreSQL server hostname
        POSTGRES_USER (str): PostgreSQL username
        POSTGRES_PASSWORD (str): PostgreSQL password
        POSTGRES_DB (str): PostgreSQL database name
        SQLALCHEMY_DATABASE_URI (Optional[str]): SQLAlchemy database URI
        DB_ECHO_LOG (bool): Enable SQLAlchemy echo logging
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Application"
    PROJECT_DESCRIPTION: str = "FastAPI application with MongoDB and PostgreSQL"
    PROJECT_VERSION: str = "0.1.0"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validate CORS origins.

        Args:
            v (Union[str, List[str]]): CORS origins value

        Returns:
            Union[List[str], str]: Validated CORS origins
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # MongoDB settings
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "fastapi_app"

    # PostgreSQL settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fastapi_app"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    DB_ECHO_LOG: bool = True

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, value: Optional[str], info) -> Any:
        """
        Assemble PostgreSQL database connection URI.

        Args:
            value (Optional[str]): Database URI value
            info: ValidationInfo object containing field data

        Returns:
            Any: Assembled database URI
        """
        if isinstance(value, str):
            return value
        data = info.data
        return (
            f"postgresql://{data.get('POSTGRES_USER')}:{data.get('POSTGRES_PASSWORD')}"
            f"@{data.get('POSTGRES_SERVER')}/{data.get('POSTGRES_DB')}"
        )

    class Config:
        """
        Settings configuration class.
        """
        case_sensitive = True
        env_file = ".env"

        # Handle paths properly for Windows and Linux
        @classmethod
        def prepare_env_path(cls, env_file: str) -> Path:
            """Convert env file string to path object."""
            return Path(env_file)


settings = Settings()
