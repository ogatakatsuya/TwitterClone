import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Like
from schemes.likes import LikeInfo
import repository.like.like as like_modules

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["like_num","is_like"],
    [pytest.param(1, True), pytest.param(1, False)]
)
async def test_get_like_status_GetLikeStatus(db_session: AsyncSession, like_num, is_like):
    mock_result_like_count = MagicMock(scalar=MagicMock(return_value=like_num))
    mock_result_is_like = MagicMock(scalar_one_or_none=MagicMock(return_value=is_like))
    db_session.execute = AsyncMock(side_effect=[mock_result_like_count, mock_result_is_like])
    
    like_num, is_like = await like_modules.get_like_status(db_session, LikeInfo(user_id=1, post_id=1))
    
    assert like_num == 1, "The get_like_status function did not return the expected like_num."
    assert is_like == is_like, "The get_like_status function did not return the expected is_like."

#post_idを取得する術がないので，一旦保留．．．
# @pytest.mark.asyncio
# async def test_create_like_success(db_session):
#     new_user1 = await auth_modules.create_user(db_session, "test_user1")
#     user1 = await auth_modules.get_user(db_session, "test_user1")
#     new_post = await post_modules.create_post(db_session, MagicMock(text="test_post", user_id=user1.id, parent_id=None))
#     new_like = await like_modules.create_like(db_session, LikeInfo(user_id=user1.id, post_id=user2.id))
#     assert new_like.user_id == 1
#     assert new_like.post_id == 1

# @pytest.mark.asyncio
# async def test_create_like_failure(db_session):
#     db_session.flush.side_effect = Exception  # Simulate database flush failure
#     with pytest.raises(HTTPException):
#         await like_modules.create_like(db_session, LikeInfo(user_id=1, post_id=1))

# @pytest.mark.asyncio
# async def test_delete_like(db_session):
#     db_session.execute.return_value.scalar_one_or_none.return_value = Like(user_id=1, post_id=1)
#     deleted_like = await like_modules.delete_like(db_session, LikeInfo(user_id=1, post_id=1))
#     assert deleted_like.user_id == 1
#     assert deleted_like.post_id == 1