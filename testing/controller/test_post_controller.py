import json

import pytest
from fastapi import HTTPException
from starlette.testclient import TestClient
from loguru import logger
from database.db_connection import get_db
from exceptions.deletion_failed_exception import DeletionFailedException
from exceptions.not_found_exception import NotFoundException
from main import app
from models import Post
from payload.user_payload import UserResponse, PostResponse, PostBase

client = TestClient(app)


@pytest.fixture
def mock_db(mocker):
    return mocker.MagicMock()


@pytest.fixture(autouse=True)
def setup_mocks(mocker):
    mock_db_session = mocker.MagicMock()
    mocker.patch('database.db_connection.get_db', return_value=mock_db_session)
    app.dependency_overrides[get_db] = lambda: mock_db_session


def test_create_post_success(mock_db, mocker):
    post_response = PostResponse(
        id=1,
        title="test title",
        content="test content",
        owner_id=1
    )
    mocker.patch('service.post_service.create_post',
                 return_value=post_response)
    post_payload = PostBase(
        title="test title",
        content="test content",
        owner_id=1
    )
    response = client.post("/posts/", json=post_payload.dict())
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == post_response.id
    assert response_data["title"] == post_response.title
    assert response_data["content"] == post_response.content
    assert response_data["owner_id"] == post_response.owner_id
    logger.info("Create post test case passed")


def test_create_post_exception(mock_db, mocker):
    mocker.patch('service.post_service.create_post',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    post_payload = PostBase(
        title="test title",
        content="test content",
        owner_id=1
    )

    response = client.post("/posts/", json=post_payload.dict())

    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Internal Server Error"
    logger.info("Create post exception test case passed")


def test_read_all_posts(mock_db, mocker):
    list_of_post = [
        {
            "id": 1, "title": "test_post", "content": "This is testing post", "owner_id": 1
        },
        {
            "id": 2, "title": "test_post 2", "content": "This is testing post2", "owner_id": 2
        }
    ]
    mocker.patch('service.post_service.get_all_post', return_value=list_of_post)
    response = client.get("/posts")
    assert response.status_code == 200

    response_json = json.loads(response.content)
    assert response_json == list_of_post

    logger.info("get all posts test case passed")


def test_read_all_posts_exception(mock_db, mocker):
    mocker.patch('service.post_service.get_all_post',
                 side_effect=HTTPException(status_code=500, detail=f"Internal Server Error"))

    response = client.get("/posts")

    assert response.status_code == 500
    assert response.json() == {"detail": f"Internal Server Error"}
    logger.info("get all post exception test case passed")


def test_get_by_id(mock_db, mocker):
    mock_post = Post(
        id=1,
        title="test_post",
        content="This is testing post",
        owner_id=1
    )
    mocker.patch('service.post_service.get_post_by_id', return_value=mock_post)
    # Remove the redundant patching of the controller function
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": mock_post.id,
        "title": mock_post.title,
        "content": mock_post.content,
        "owner_id": mock_post.owner_id
    }
    logger.info("get post by id test case passed")


def test_get_by_id_not_found(mock_db, mocker):
    mocker.patch('service.post_service.get_post_by_id',
                 side_effect=NotFoundException(status_code=404, detail=f"Post not found with id: 1"))

    response = client.get("/posts/1")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Post not found with id: 1"}
    logger.info("get post by id not found exception test case passed")


def test_get_by_id_exception(mock_db, mocker):
    mocker.patch('service.post_service.get_post_by_id',
                 side_effect=HTTPException(status_code=500, detail=f"Internal Server Error"))

    response = client.get("/posts/1")

    assert response.status_code == 500
    assert response.json() == {"detail": f"Internal Server Error"}
    logger.info("get post by id exception test case passed")


def test_delete_post_success(mock_db, mocker):
    mocker.patch('service.post_service.delete_post',
                 return_value='Delete successful')
    response = client.delete("/posts/1")
    assert response.status_code == 200

    response_content = response.content.decode().strip('"')
    assert response_content == "Delete successful"
    logger.info("delete post by id success test case passed")


def test_delete_post_not_found(mock_db, mocker):
    mocker.patch('service.post_service.delete_post',
                 side_effect=NotFoundException(status_code=404, detail="Post not found with id: 1"))

    response = client.delete("/posts/1")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Post not found with id: 1"}
    logger.info("delete post by id not found exception test case passed")


def test_delete_post_exception(mock_db, mocker):
    mocker.patch('service.post_service.delete_post',
                 side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    response = client.delete("/posts/1")
    assert response.status_code == 500
    assert response.json() == {"detail": f"Internal Server Error"}
    logger.info("delete post by id exception test case passed")


def test_delete_post_deletion_exception(mock_db, mocker):
    mocker.patch('service.post_service.delete_post',
                 side_effect=DeletionFailedException(status_code=500, detail="Deletion failed"))

    response = client.delete("/posts/1")
    assert response.status_code == 500
    assert response.json() == {"detail": f"Deletion failed"}
    logger.info("delete post by id exception test case passed")
