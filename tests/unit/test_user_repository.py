import pytest
from unittest.mock import AsyncMock, MagicMock
from app.db.repositories.user import UserRepository
from app.models.user import User, UserCreate, UserUpdate

import pytest_asyncio

@pytest_asyncio.fixture
def db_session():
    return AsyncMock()

@pytest_asyncio.fixture
def user():
    return User(id=1, email="test@example.com", hashed_password="hashed", is_active=True, full_name="Test User")

@pytest.mark.asyncio
async def test_get_by_id(db_session, user):
    repo = UserRepository()
    db_session.exec.return_value.first.return_value = user
    result = await repo.get(db_session, user_id=1)
    assert result == user
    db_session.exec.assert_awaited()

@pytest.mark.asyncio
async def test_get_by_email(db_session, user):
    repo = UserRepository()
    db_session.exec.return_value.first.return_value = user
    result = await repo.get_by_email(db_session, email="test@example.com")
    assert result == user
    db_session.exec.assert_awaited()

@pytest.mark.asyncio
async def test_get_all(db_session, user):
    repo = UserRepository()
    db_session.exec.return_value.all.return_value = [user]
    result = await repo.get_all(db_session)
    assert result == [user]
    db_session.exec.assert_awaited()

@pytest.mark.asyncio
async def test_create(db_session):
    repo = UserRepository()
    user_in = UserCreate(email="test@example.com", password="pw", full_name="Test User")
    db_session.commit = AsyncMock()
    db_session.refresh = AsyncMock()
    db_session.add = MagicMock()
    result = await repo.create(db_session, obj_in=user_in)
    db_session.add.assert_called()
    db_session.commit.assert_awaited()
    db_session.refresh.assert_awaited()
    assert isinstance(result, User)

@pytest.mark.asyncio
async def test_update(db_session, user):
    repo = UserRepository()
    user_update = UserUpdate(email="new@example.com")
    db_session.commit = AsyncMock()
    db_session.refresh = AsyncMock()
    db_session.add = MagicMock()
    result = await repo.update(db_session, db_obj=user, obj_in=user_update)
    db_session.add.assert_called()
    db_session.commit.assert_awaited()
    db_session.refresh.assert_awaited()
    assert result.email == "new@example.com"

@pytest.mark.asyncio
async def test_delete(db_session, user):
    repo = UserRepository()
    repo.get = AsyncMock(return_value=user)
    db_session.delete = AsyncMock()
    db_session.commit = AsyncMock()
    result = await repo.delete(db_session, id=1)
    db_session.delete.assert_awaited_with(user)
    db_session.commit.assert_awaited()
    assert result == user

@pytest.mark.asyncio
async def test_delete_not_found(db_session):
    repo = UserRepository()
    repo.get = AsyncMock(return_value=None)
    db_session.delete = AsyncMock()
    db_session.commit = AsyncMock()
    result = await repo.delete(db_session, id=2)
    db_session.delete.assert_not_awaited()
    db_session.commit.assert_not_awaited()
    assert result is None
