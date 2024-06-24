import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Follow
from schemes.follow import FollowBody
import repository.follow.follow as follow_modules

@pytest.mark.asyncio #followの作成部分をmock化していいのか？でもuser_idがないとintegrityerrorが出る．．．
async def test_follow_success(db_session: AsyncSession):
    follow_body = FollowBody(user_id=1, follow_id=2)

    with patch.object(db_session, 'add', new=AsyncMock()) as mock_add:
        await follow_modules.follow(db_session, follow_body)
        mock_add.assert_called_once()

@pytest.mark.asyncio
async def test_delete_follow(db_session):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=Follow(follow_id=1, followed_id=2))))
    follow_body = FollowBody(user_id=1, follow_id=2)
    with patch.object(db_session, 'delete', new=AsyncMock()) as mock_delete:
        await follow_modules.delete_follow(db_session, follow_body)
        mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_count_following_users(db_session):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar=MagicMock(return_value=10)))
    result = await follow_modules.count_following_users(db_session, 1)
    assert result == 10, "The count_following_users function did not return the expected result."

@pytest.mark.asyncio
async def test_count_followed_users(db_session):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar=MagicMock(return_value=5)))
    result = await follow_modules.count_followed_users(db_session, 1)
    assert result == 5

@pytest.mark.asyncio
async def test_is_follow_following(db_session):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=Follow(follow_id=1, followed_id=2))))
    follow_body = FollowBody(user_id=1, follow_id=2)
    result = await follow_modules.is_follow(db_session, follow_body)
    assert result is not None
    
@pytest.mark.asyncio
async def test_is_follow_not_following(db_session):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
    follow_body = FollowBody(user_id=1, follow_id=2)
    result = await follow_modules.is_follow(db_session, follow_body)
    assert result is None