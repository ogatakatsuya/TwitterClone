import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from models.models import Post, User
import repository.posts.posts as post_modules
import repository.auth.user as auth_modules

@pytest.mark.asyncio
async def test_create_post_MakeNewPost_ReturnNewPost(db_session: AsyncSession):
    await auth_modules.create_user(db_session, "test_user")
    new_user = await auth_modules.get_user(db_session, "test_user")
    user_id = new_user.id
    test_post = "test_post"
    post_body = MagicMock(text=test_post, user_id=user_id, parent_id=None)
    
    post = await post_modules.create_post(db_session, post_body)
    
    assert post.text == test_post
    assert post.user_id == user_id

@pytest.mark.asyncio
async def test_get_post_GetSinglePost_ReturnSinglePost(db_session: AsyncSession):
    expected_post_id = 1
    excepted_text = "Test Post"
    expected_user_name = "User1"
    db_session.execute = AsyncMock(return_value=MagicMock(first=MagicMock(return_value=(Post(id=expected_post_id, text=excepted_text, user_id=1, parent_id=None), expected_user_name))))
    
    post = await post_modules.get_post(db_session, expected_post_id)
    
    assert post is not None
    assert post['id'] == expected_post_id
    assert post['text'] == excepted_text
    assert post['user_name'] == expected_user_name
    
@pytest.mark.asyncio
async def test_get_post_GetSinglePost_ReturnNone(db_session: AsyncSession):
    db_session.execute = AsyncMock(return_value=MagicMock(first=MagicMock(return_value=(None, "User1"))))
    post = await post_modules.get_post(db_session, 1)
    assert post is None

@pytest.mark.asyncio
async def test_delete_post_DeleteSinglePost_ReturnTrue(db_session: AsyncSession):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=Post(id=1))))
    db_session.delete = AsyncMock()
    result = await post_modules.delete_post(db_session, 1)
    assert result == True
    db_session.delete.assert_called_once()