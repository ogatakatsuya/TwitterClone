import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from models.models import Post, User
import repository.posts.posts as post_modules

@pytest.mark.asyncio
async def test_create_post(db_session: AsyncSession):
    post_body = MagicMock(text="Test Post", user_id=4, parent_id=None)
    post = await post_modules.create_post(db_session, post_body)
    assert post.text == post_body.text
    assert post.user_id == post_body.user_id
    assert post.parent_id == post_body.parent_id

@pytest.mark.asyncio
async def test_get_post_success(db_session: AsyncSession):
    db_session.execute = AsyncMock(return_value=MagicMock(first=MagicMock(return_value=(Post(id=1, text="Test Post", user_id=1, parent_id=None), "User1"))))
    post = await post_modules.get_post(db_session, 1)
    assert post is not None
    assert post['id'] == 1
    assert post['text'] == "Test Post"
    assert post['user_name'] == "User1"
    
@pytest.mark.asyncio
async def test_get_post_failure(db_session: AsyncSession):
    db_session.execute = AsyncMock(return_value=MagicMock(first=MagicMock(return_value=(None, "User1"))))
    post = await post_modules.get_post(db_session, 1)
    assert post is None

@pytest.mark.asyncio
async def test_delete_post(db_session: AsyncSession):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=Post(id=1))))
    db_session.delete = AsyncMock()
    result = await post_modules.delete_post(db_session, 1)
    assert result == True
    db_session.delete.assert_called_once()