import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Follow
from schemes.follow import FollowBody
import repository.follow.follow as follow_modules
import repository.auth.user as auth_modules

@pytest.mark.asyncio
async def test_follow_success(db_session: AsyncSession):
    test_user1 = "test_user1"
    test_user2 = "test_user2"
    await auth_modules.create_user(db_session, test_user1)
    await auth_modules.create_user(db_session, test_user2)
    user1 = await auth_modules.get_user(db_session, test_user1)
    user2 = await auth_modules.get_user(db_session, test_user2)
    follow_body = FollowBody(user_id=user1.id, follow_id=user2.id)
    
    new_follow = await follow_modules.follow(db_session, follow_body)
    
    assert new_follow.follow_id == user1.id
    assert new_follow.followed_id == user2.id

@pytest.mark.asyncio
async def test_delete_follow_DeleteFollow(db_session):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=Follow(follow_id=1, followed_id=2))))
    follow_body = FollowBody(user_id=1, follow_id=2)
    with patch.object(db_session, 'delete', new=AsyncMock()) as mock_delete:
        await follow_modules.delete_follow(db_session, follow_body)
        mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_count_following_users_CountFollow_ReturnFollowsNum(db_session):
    follows_num = 0
    db_session.execute = AsyncMock(return_value=MagicMock(scalar=MagicMock(return_value=follows_num)))
    
    result = await follow_modules.count_following_users(db_session, 1)
    
    assert result == follows_num, "The count_following_users function did not return the expected result."

@pytest.mark.asyncio
async def test_count_followed_CountFollower_ReturnFollowersNum(db_session):
    followers_num = 0
    db_session.execute = AsyncMock(return_value=MagicMock(scalar=MagicMock(return_value=followers_num)))
    
    result = await follow_modules.count_followed_users(db_session, 1)
    
    assert result == followers_num, "The count_followed_users function did not return the expected result."

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["expected","follow_record"],
    [pytest.param(True,Follow(follow_id=1, followed_id=2)), pytest.param(False,None)]
)
async def test_is_follow_following_ConfirmIsFollow(db_session, expected,follow_record):
    db_session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=follow_record)))
    follow_body = FollowBody(user_id=1, follow_id=2)
    
    is_follow = await follow_modules.is_follow(db_session, follow_body)
    
    assert is_follow == expected, "The is_follow function did not return the expected result."