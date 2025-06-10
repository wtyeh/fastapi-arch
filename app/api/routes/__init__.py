"""
API router module.
"""
from fastapi import APIRouter

from app.api.routes import users, logs, data_analysis

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(logs.router, prefix="/logs", tags=["logs"])
router.include_router(data_analysis.router, prefix="/data-analysis", tags=["data-analysis"])