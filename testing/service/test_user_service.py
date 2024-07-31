import pytest

from loguru import logger

from exceptions.deletion_failed_exception import DeletionFailedException
from models import User
from payload.user_payload import UserResponse, UserRequest
from service import user_service
from exceptions.not_found_exception import NotFoundException


@pytest.fixture
def mock_db(mocker):
    return mocker.MagicMock()

# @pytest.fixture(autouse=True)
# def print_statements():
#     logger.info("\n--- Starting Test Case ---")
#     yield
#     logger.error("--- Ending Test Case ---")


def test_get_user_found(mock_db, mocker):
    mock_user = mocker.MagicMock()
    mock_user.id = 1
    mock_user.username = "test_user"

    mocker.patch('repositories.user_repo.get_user', return_value=mock_user)
    user_id = 1
    user = user_service.get_user(mock_db, user_id)

    # Assertions
    assert user.id == 1
    assert user.username == "test_user"
    logger.info("get user by id test case pass")


def test_get_user_not_found(mock_db, mocker):
    user_id = 1

    mocker.patch('repositories.user_repo.get_user', return_value=None)

    with pytest.raises(NotFoundException) as exc_info:
        user_service.get_user(mock_db, user_id)

    # Assertions
    assert exc_info.value.status_code == 404
    assert str(exc_info.value.detail) == f"User not found with id : {user_id}"
    logger.info("get user by id not found exception test case pass")


def test_get_all_users(mock_db, mocker):
    list_of_users = [
        {
            "id": 1, "username": "Abhishek", "disabled": False
        },
        {
            "id": 2, "username": "Kartik", "disabled": False
        }
    ]
    mocker.patch('repositories.user_repo.get_users', return_value=list_of_users)
    users = user_service.get_users(mock_db)
    assert users == list_of_users
    logger.info("get all users test case pass")


def test_create_user_success_test_(mock_db, mocker):
    # Prepare the input data
    username = "test_user"
    password = "hashed_password"

    # Create a mock user object
    mock_user = mocker.MagicMock()
    mock_user.id = 1
    mock_user.username = username
    mock_user.disabled = False

    # Mock the user_repo.create_user function
    mocker.patch('repositories.user_repo.create_user', return_value=mock_user)

    # Call the service layer function
    result = user_service.create_user(mock_db, username, password)

    # Assertions
    assert result.id == 1
    assert result.username == "test_user"
    assert result.disabled == False

    logger.info(f"create user test case pass {mock_user}")


def test_create_user_failure_test(mock_db, mocker):
    # Prepare the input data
    username = "test_user"
    password = "hashed_password"

    # Mock the user_repo.create_user function to raise an exception
    mocker.patch('repositories.user_repo.create_user', side_effect=Exception("Database error"))

    # Call the service layer function and assert that an exception is raised
    with pytest.raises(Exception) as exc_info:
        user_service.create_user(mock_db, username, password)

    assert str(exc_info.value) == "Database error"
    mock_db.rollback.assert_called_once()

    logger.info(f"create user failure test case passed with exception: {exc_info.value}")


def test_get_user_by_name(mock_db, mocker):
    test_user = UserResponse(
        id=1,
        username="test_user",
        disabled=False
    )
    mocker.patch('repositories.user_repo.get_by_name', return_value=test_user)

    user = user_service.get_by_name(mock_db, "test_user")
    assert user == test_user


def test_get_user_by_name_not_found(mock_db, mocker):
    username = "test_user"
    mocker.patch('repositories.user_repo.get_by_name', return_value=None)
    with pytest.raises(NotFoundException) as ex:
        user_service.get_by_name(mock_db, username)
    assert ex.value.status_code == 404
    assert str(ex.value.detail) == f"User not found with name : {username}"


def test_get_all_users_name(mock_db, mocker):
    mock_user_names = [
        {"username": "Abhi"},
        {"username": "Kartik"}
    ]
    mocker.patch('repositories.user_repo.get_all_users_name', return_value=mock_user_names)
    response = (user_service.get_users_name(mock_db))
    assert response == mock_user_names


def test_delete_user_success(mock_db, mocker):
    mocker.patch('repositories.user_repo.delete_user', return_value=1)
    result = user_service.delete_user(mock_db, 1)
    assert result == 'Delete successful'
    logger.info(f"User delete test case pass ")


def test_delete_user_fail(mock_db, mocker):
    # Mock the delete_user method to return 0, simulating a deletion failure
    mocker.patch('repositories.user_repo.delete_user', return_value=0)

    # Assert that DeletionFailedException is raised
    with pytest.raises(DeletionFailedException) as exc_info:
        user_service.delete_user(mock_db, 1)

    # Check the exception details
    assert exc_info.value.status_code == 500
    assert str(exc_info.value.detail) == "Failed to delete user with ID: 1"
    logger.info("Deletion failed as expected with exception: %s", exc_info.value)


def test_delete_user_exception(mock_db, mocker):
    # Mock the user_repo.create_user function to raise an exception
    mocker.patch('repositories.user_repo.delete_user', side_effect=Exception("Internal server error"))

    # Call the service layer function and assert that an exception is raised
    with pytest.raises(Exception) as exc_info:
        user_service.delete_user(mock_db, 1)

    assert str(exc_info.value) == "Internal server error"
    mock_db.rollback.assert_called_once()

    logger.info(f"delete user failure test case passed with exception: {exc_info.value}")


def test_update_user_success(mock_db, mocker):
    update_user = User(
        id=1,
        username="test_user",
        disabled=False
    )
    # Patch the correct path to the repository function
    mocker.patch('repositories.user_repo.update_user',
                 return_value=update_user)

    user_payload = UserRequest(
        username="test_user",  # Corrected the typo here
        password="1234"
    )

    # Call the service layer function
    result = user_service.update_user(mock_db, 1, user_payload)

    # Assertions
    assert result.id == 1
    assert result.username == "test_user"
    assert result.disabled == False


def test_update_user_exception(mock_db, mocker):
    # Mock the user_repo.create_user function to raise an exception
    mocker.patch('repositories.user_repo.update_user', side_effect=Exception("Internal server error"))

    user_payload = UserRequest(
        username="test_user",  # Corrected the typo here
        password="1234"
    )

    # Call the service layer function and assert that an exception is raised
    with pytest.raises(Exception) as exc_info:
        user_service.update_user(mock_db, 1, user_payload)

    assert str(exc_info.value) == "Internal server error"
    mock_db.rollback.assert_called_once()

    logger.info(f"update user failure test case passed with exception: {exc_info.value}")









