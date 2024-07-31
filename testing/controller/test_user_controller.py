import json

import pytest
from fastapi import HTTPException
from starlette.testclient import TestClient
from loguru import logger
from database.db_connection import get_db
from exceptions.not_found_exception import NotFoundException
from main import app
from models import User
from payload.user_payload import UserResponse

client = TestClient(app)


@pytest.fixture
def mock_db(mocker):
    return mocker.MagicMock()


@pytest.fixture(autouse=True)
def setup_mocks(mocker):
    mock_db_session = mocker.MagicMock()
    mocker.patch('database.db_connection.get_db', return_value=mock_db_session)
    app.dependency_overrides[get_db] = lambda: mock_db_session


def test_create_user(mock_db, mocker):
    test_user = UserResponse(
        id=1,
        username="test_user",
        disabled=False
    )
    mocker.patch('service.user_service.create_user',
                 return_value=test_user)

    user_payload = {
        "username": "test_user",
        "password": "1234"
    }
    response = client.post("/users/", json=user_payload)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == test_user.id
    assert response_data["username"] == test_user.username
    assert response_data["disabled"] == test_user.disabled
    logger.info("Create user test case passed")


def test_create_user_exception(mock_db, mocker):
    mocker.patch('service.user_service.create_user',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    user_payload = {
        "username": "test_user",
        "password": "1234"
    }

    response = client.post("/users/", json=user_payload)

    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("Create user exception test case passed")


def test_read_user(mock_db, mocker):
    test_user = User(
        id=1,
        username="test_user",
        hashed_password="1234"
    )
    mocker.patch('service.user_service.get_user', return_value=test_user)
    # Remove the redundant patching of the controller function
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "username": test_user.username,
        "hashed_password": test_user.hashed_password
    }
    logger.info("Read user success test case passed")


def test_read_user_not_found(mock_db, mocker):
    mocker.patch('service.user_service.get_user',
                 side_effect=NotFoundException(status_code=404, detail="User not found with id: 1"))

    response = client.get("/users/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found with id: 1"}
    logger.info("Read user not found exception test case passed")


def test_read_user_exception(mock_db, mocker):
    mocker.patch('service.user_service.get_user',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    response = client.get("/users/1")
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("Read user exception test case passed")


def test_read_all_users(mock_db, mocker):
    mock_users = [
        {"id": 1, "username": "test_user", "hashed_password": "1234"},
        {"id": 2, "username": "test_user2", "hashed_password": "1234"}
    ]
    mocker.patch('service.user_service.get_users', return_value=mock_users)
    response = client.get("/users")
    assert response.status_code == 200

    response_json = json.loads(response.content)
    assert response_json == mock_users

    logger.info("get all users test case passed")


def test_read_all_users_exception(mock_db, mocker):
    mocker.patch('service.user_service.get_users',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    response = client.get("/users")
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("Read all users exception test case passed")


def test_read_user_by_name(mock_db, mocker):
    test_user = UserResponse(
        id=1,
        username="test_user",
        disabled=False
    )
    mocker.patch('service.user_service.get_by_name', return_value=test_user)
    # Remove the redundant patching of the controller function
    response = client.get("/users/users_name/test_user")
    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "username": test_user.username,
        "disabled": test_user.disabled
    }
    logger.info("get user by name success test case passed")


def test_read_user_by_name_not_found(mock_db, mocker):
    mocker.patch('service.user_service.get_by_name',
                 side_effect=NotFoundException(status_code=404, detail="User not found with username: test_user"))

    response = client.get("/users/users_name/test_user")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found with username: test_user"}
    logger.info("get user by name not found exception test case passed")


def test_read_user_by_name_exception(mock_db, mocker):
    mocker.patch('service.user_service.get_by_name',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    response = client.get("/users/users_name/test_user")
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("get user by name exception test case passed")


def test_get_all_users_name(mock_db, mocker):
    mock_user_names = [
        {"username": "Abhi"},
        {"username": "Kartik"}
    ]
    mocker.patch('service.user_service.get_users_name', return_value=mock_user_names)
    response = client.get("/users/all_name/users_name")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == mock_user_names
    logger.info("get all users name success test case passed")


def test_get_all_users_name_exception(mock_db, mocker):
    mocker.patch('service.user_service.get_users_name',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))
    response = client.get("/users/all_name/users_name")
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("get all users name exception test case passed")


def test_delete_user_success(mock_db, mocker):
    mocker.patch('service.user_service.delete_user',
                 return_value=1)
    response = client.delete("/users/1")
    assert response.status_code == 200
    logger.info("delete user by id success test case passed")


def test_delete_user_not_found(mock_db, mocker):
    mocker.patch('service.user_service.delete_user',
                 side_effect=NotFoundException(status_code=404, detail="User not found with id: 1"))

    response = client.delete("/users/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found with id: 1"}
    logger.info("delete user by id not found exception test case passed")


def test_delete_user_exception(mock_db, mocker):
    mocker.patch('service.user_service.delete_user',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))
    response = client.delete("/users/1")
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("delete user by id exception test case passed")


def test_update_user_success(mock_db, mocker):
    update_user = UserResponse(
        id=1,
        username="test_user",
        disabled=False
    )
    mocker.patch('service.user_service.update_user',
                 return_value=update_user)

    user_payload = {
        "username": "test_user",
        "password": "1234"
    }
    response = client.put("/users/update/1", json=user_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == update_user.id
    assert response_data["username"] == update_user.username
    assert response_data["disabled"] == update_user.disabled
    logger.info("Update user test case passed")


def test_update_user_not_found(mock_db, mocker):
    mocker.patch('service.user_service.update_user',
                 side_effect=NotFoundException(status_code=404, detail="User not found with id: 1"))

    user_payload = {
        "username": "test_user",
        "password": "1234"
    }
    response = client.put("/users/update/1", json=user_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found with id: 1"}
    logger.info("Update user by id not found exception test case passed")









