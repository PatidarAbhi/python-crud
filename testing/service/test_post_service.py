import pytest

from loguru import logger

from exceptions.deletion_failed_exception import DeletionFailedException
from models import Post
from payload.user_payload import UserResponse, PostBase, PostResponse, UpdatePostPayload
from service import post_service
from exceptions.not_found_exception import NotFoundException


@pytest.fixture
def mock_db(mocker):
    return mocker.MagicMock()


def test_get_post_found(mock_db, mocker):
    list_of_post = [
        {
            "id": 1, "title": "test_post", "content": "This is testing post", "owner_id": 1
        },
        {
            "id": 2, "title": "test_post 2", "content": "This is testing post2", "owner_id": 2
        }
    ]
    mocker.patch('repositories.post_repo.get_all_post', return_value=list_of_post)
    posts = post_service.get_all_post(mock_db)
    assert posts == list_of_post
    # Assertions
    logger.info("get all post test case pass")


def test_get_post_found_not_found(mock_db, mocker):
    mocker.patch('repositories.post_repo.get_all_post', return_value=None)
    with pytest.raises(NotFoundException) as ex:
        posts = post_service.get_all_post(mock_db)

    assert ex.value.status_code == 404
    assert str(ex.value.detail) == f"Posts not found"

    logger.info("get all post not found test case pass")


def test_create_post_success_test_(mock_db, mocker):
    post_request = PostBase(
        title="test post",
        content="This is posting test",
        owner_id=1
    )

    mock_post = PostResponse(
        id=1,
        title="test post",
        content="This is testing test",
        owner_id=1
    )

    # Mock the user_repo.create_user function
    mocker.patch('repositories.post_repo.create_post', return_value=mock_post)

    # Call the service layer function
    result = post_service.create_post(mock_db, post_request)

    # Assertions
    assert result.id == 1
    assert result.title == "test post"
    assert result.content == "This is testing test"
    assert result.owner_id == 1


def test_get_post_by_id(mock_db, mocker):
    mock_post = Post(
        id=1,
        title="test_post",
        content="This is testing post",
        owner_id=1
    )
    mocker.patch('repositories.post_repo.get_post_by_id', return_value=mock_post)
    post = post_service.get_post_by_id(mock_db, 1)
    assert post == mock_post
    # Assertions
    logger.info("get post by id test case pass")


def test_get_post_by_id_not_found(mock_db, mocker):
    mocker.patch('repositories.post_repo.get_post_by_id', return_value=None)
    post_id = 1
    with pytest.raises(NotFoundException) as exc_info:
        post_service.get_post_by_id(mock_db, post_id)

    # Assertions
    assert exc_info.value.status_code == 404
    assert str(exc_info.value.detail) == f"Post not found with id : {post_id}"


def test_delete_post_success(mock_db, mocker):
    mocker.patch('repositories.post_repo.delete_post', return_value=1)
    result = post_service.delete_post(mock_db, 1)
    assert result == 'Delete successful'
    logger.info(f"Post delete test case pass ")


def test_delete_post_fail(mock_db, mocker):
    # Mock the delete_post method to return 0, simulating a deletion failure
    mocker.patch('repositories.post_repo.delete_post', return_value=0)

    # Assert that DeletionFailedException is raised
    with pytest.raises(DeletionFailedException) as exc_info:
        post_service.delete_post(mock_db, 1)

    # Check the exception details
    assert exc_info.value.status_code == 500
    assert str(exc_info.value.detail) == "Failed to delete post with ID: 1"
    logger.info("Post deletion failed as expected with exception: %s", exc_info.value)


def test_update_post_success(mock_db, mocker):
    update_post = Post(
        id=1,
        title="updated title",
        content="updated content"
    )
    # Patch the correct path to the repository function
    mocker.patch('repositories.post_repo.update_post',
                 return_value=update_post)

    post_payload = UpdatePostPayload(
        title="updated title",
        content="updated content"
    )

    # Call the service layer function
    result = post_service.update_post(mock_db, 1, post_payload)

    # Assertions
    assert result.id == 1
    assert result.title == "updated title"
    assert result.content == "updated content"
    logger.info("Post update success test case passed")
