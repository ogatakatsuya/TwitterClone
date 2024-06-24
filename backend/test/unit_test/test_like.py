import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Like
from schemes.likes import LikeInfo
import repository.like.like as like_modules

@pytest.mark.asyncio
async def test_get_like_status_like(db_session: AsyncSession):
    mock_result_like_count = MagicMock(scalar=MagicMock(return_value=1))
    mock_result_is_like = MagicMock(scalar_one_or_none=MagicMock(return_value=Like(user_id=1, post_id=1)))
    db_session.execute = AsyncMock(side_effect=[mock_result_like_count, mock_result_is_like])
    
    like_num, is_like = await like_modules.get_like_status(db_session, LikeInfo(user_id=1, post_id=1))
    
    assert like_num == 1, "The get_like_status function did not return the expected like_num."
    assert is_like is True, "The get_like_status function did not return the expected is_like."

@pytest.mark.asyncio
async def test_get_like_status_not_like(db_session: AsyncSession):
    mock_result_like_count = MagicMock(scalar=MagicMock(return_value=1))
    mock_result_is_like = MagicMock(scalar_one_or_none=MagicMock(return_value=None))
    db_session.execute = AsyncMock(side_effect=[mock_result_like_count, mock_result_is_like])
    like_num, is_like = await like_modules.get_like_status(db_session, LikeInfo(user_id=1, post_id=1))
    assert like_num == 1, "The get_like_status function did not return the expected like_num."
    assert is_like is False, "The get_like_status function did not return the expected is_like."

#これもuser_idが必要なのでaddをmockにするしかないのか．．？
# @pytest.mark.asyncio
# async def test_create_like_success(db_session):
#     new_like = await like_modules.create_like(db_session, LikeInfo(user_id=1, post_id=1))
#     assert new_like.user_id == 1
#     assert new_like.post_id == 1

# @pytest.mark.asyncio
# async def test_create_like_failure(db_session):
#     db_session.flush.side_effect = Exception  # Simulate database flush failure
#     with pytest.raises(HTTPException):
#         await like_modules.create_like(db_session, LikeInfo(user_id=1, post_id=1))

# @pytest.mark.asyncio
# async def test_delete_like(db_session):
#     db_session.execute.return_value.scalar_one_or_none.return_value = Like(user_id=1, post_id=1)  # Mock finding the like
#     deleted_like = await like_modules.delete_like(db_session, LikeInfo(user_id=1, post_id=1))
#     assert deleted_like.user_id == 1
#     assert deleted_like.post_id == 1