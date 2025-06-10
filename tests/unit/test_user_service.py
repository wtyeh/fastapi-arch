import asyncio
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.user import UserService
from app.models.user import User, UserCreate, UserUpdate

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.get = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.get_by_email = AsyncMock()
    return repo

@pytest.fixture
def user_service(mock_repository):
    return UserService(repository=mock_repository)

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.fixture
def user():
    return User(id=1, email="test@example.com", hashed_password="hashed", is_active=True, full_name="Test User")


@pytest.mark.asyncio
async def test_get_user(user_service, mock_repository, db_session, user):
    mock_repository.get.return_value = user
    result = await user_service.get(db_session, user_id=1)
    assert result == user
    mock_repository.get.assert_called_once_with(db_session, 1)

@pytest.mark.asyncio
async def test_get_all_users(user_service, mock_repository, db_session, user):
    mock_repository.get_all.return_value = [user]
    result = await user_service.get_all(db_session)
    assert result == [user]
    mock_repository.get_all.assert_called_once_with(db_session, skip=0, limit=100)

@pytest.mark.asyncio
async def test_update_user(user_service, mock_repository, db_session, user):
    user_update = UserUpdate(email="new@example.com")
    updated_user = User(id=1, email="new@example.com", hashed_password="hashed", is_active=True, full_name="New User")
    mock_repository.update.return_value = updated_user
    result = await user_service.update(db_session, db_obj=user, obj_in=user_update)
    assert result == updated_user
    mock_repository.update.assert_awaited_once_with(db_session, db_obj=user, obj_in=user_update)

@pytest.mark.asyncio
async def test_delete_user(user_service, mock_repository, db_session, user):
    mock_repository.delete.return_value = user
    result = await user_service.delete(db_session, user_id=1)
    assert result == user
    mock_repository.delete.assert_awaited_once_with(db_session, id=1)


@pytest.mark.asyncio
async def test_delete_returns_deleted_user(user_service, mock_repository, db_session, user):
    user_id = 1
    deleted_user = User(id=user_id, email="test@example.com", hashed_password="hashed", full_name="Test User")
    mock_repository.delete.return_value = deleted_user

    result = await user_service.delete(db_session, user_id=user_id)

    mock_repository.delete.assert_awaited_once_with(db_session, id=user_id)
    assert result == deleted_user

@pytest.mark.asyncio
async def test_delete_returns_none_when_user_not_found(user_service, mock_repository, db_session):
    user_id = 2
    mock_repository.delete.return_value = None

    result = await user_service.delete(db_session, user_id=user_id)

    mock_repository.delete.assert_awaited_once_with(db_session, id=user_id)
    assert result is None

@pytest.mark.asyncio
async def test_authenticate_success(user_service, db_session, user):
    with patch.object(user_service, "get_by_email", AsyncMock(return_value=user)):
        with patch("app.services.user.verify_password", return_value=True):
            result = await user_service.authenticate(db_session, email="test@example.com", password="password")
    assert result == user

@pytest.mark.asyncio
async def test_authenticate_user_not_found(user_service, db_session):
    with patch.object(user_service, "get_by_email", AsyncMock(return_value=None)):
        result = await user_service.authenticate(db_session, email="notfound@example.com", password="password")
    assert result is None

@pytest.mark.asyncio
async def test_authenticate_wrong_password(user_service, db_session, user):
    with patch.object(user_service, "get_by_email", AsyncMock(return_value=user)):
        with patch("app.services.user.verify_password", return_value=False):
            result = await user_service.authenticate(db_session, email="test@example.com", password="wrong")
    assert result is None

@pytest.mark.asyncio
async def test_get_by_email_returns_user(user_service, mock_repository, db_session):
    user = User(id=1, email="test@example.com", hashed_password="hashed", full_name="Test User")
    mock_repository.get_by_email.return_value = user

    result = await user_service.get_by_email(db_session, "test@example.com")

    mock_repository.get_by_email.assert_awaited_once_with(db_session, "test@example.com")
    assert result == user

@pytest.mark.asyncio
async def test_get_by_email_returns_none_when_not_found(user_service, mock_repository, db_session):
    mock_repository.get_by_email.return_value = None

    result = await user_service.get_by_email(db_session, "notfound@example.com")

    mock_repository.get_by_email.assert_awaited_once_with(db_session, "notfound@example.com")
    assert result is None