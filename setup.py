from setuptools import find_packages, setup

setup(
    name="fastapi-app",
    version="0.1.0",
    description="FastAPI application with MongoDB and PostgreSQL",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.23.2",
        "sqlmodel>=0.0.8",
        "motor>=3.3.1",
        "pandas>=2.1.1",
        "pydantic>=2.4.2",
        "pydantic-settings>=2.0.3",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.6",
        "email-validator>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
            "black>=23.9.1",
            "isort>=5.12.0",
            "pre-commit>=3.5.0",
        ],
    },
)
