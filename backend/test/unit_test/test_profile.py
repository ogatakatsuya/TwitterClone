import pytest
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import repository.user.user as profile_modules
from unittest.mock import AsyncMock, MagicMock
from schemes.profile import NewProfile
from models.models import User

@pytest.mark.asyncio
async def test_get_profile(db_session: AsyncSession):
    mock_user = User(id=1, nickname="test_nickname", biography="test_biography", birth_day="2000-01-01")
    db_session.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_user)))))
    profile = await profile_modules.get_profile(db_session, 1)
    
    assert profile.id == mock_user.id
    assert profile.nickname == mock_user.nickname
    assert profile.biography == mock_user.biography
    assert profile.birth_day == mock_user.birth_day
    
# @pytest.mark.asyncio
# async def test_edit_profile(db_session: AsyncSession):
#     user_id = 1
#     new_nickname = "UpdatedUser"
#     new_biography = "Updated Bio"
#     new_birth_day = "2001-01-01"
#     profile_body = NewProfile(user_id=user_id, nickname=new_nickname, biography=new_biography, birth_day=new_birth_day)
    
#     # Mock user data and database response
#     mock_user = User(id=user_id, nickname="TestUser", biography="Test Bio", birth_day="2000-01-01")
#     db_session.execute.return_value.scalars().first.return_value = mock_user
    
#     # Invoke edit_profile
#     result = await profile_modules.edit_profile(db_session, profile_body)
    
#     # Verify changes
#     assert result == True
#     assert mock_user.nickname == new_nickname
#     assert mock_user.biography == new_biography
#     assert mock_user.birth_day == new_birth_day