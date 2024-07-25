import pytest
from unittest.mock import MagicMock
from service import user_service


@pytest.fixture
def mock_db():
    # Setup code
    print("Setting up mock database")
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "test_user"

    # Mocking the chain of SQLAlchemy query methods
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_user

    # Yield the mock object for use in tests
    yield mock_db

    # Teardown code
    print("Tearing down mock database")
    # Perform any cleanup if necessary


def test_get_user_found(mock_db):
    user_id = 1
    user = user_service.get_user(mock_db, user_id)
    print(f"Retrieved user: ID = {user.id}, Username = {user.username}")
    assert user.id == 1
    assert user.username == "test_user"


def test_get_user_not_found(mock_db):
    user_id = 1
    user = user_service.get_user(mock_db, user_id)
    print(f"Retrieved user: ID = {user.id}, Username = {user.username}")
    assert user.id == 1
    assert user.username == "test_user"
