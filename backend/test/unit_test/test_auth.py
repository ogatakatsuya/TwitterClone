import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import repository.auth.user as auth_modules
import schemes.auth as auth_schemes
from models.models import User, Password
from repository.auth.user import SECRET_KEY, ALGORITHM
from jose import jwt

def test_get_password_hash():
    password = "test_password"
    hashed_password = auth_modules.get_password_hash(password)
    assert hashed_password != password, "failed at get_password_hash"

@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        pytest.param({"correct_password": "test_password", "input_password": "test_password"}, True),
        pytest.param({"correct_password": "test_password", "input_password": "wrong_password"}, False)
    ]
)
def test_verify_password_VerifyInputPasswordWithHedhedPassword(test_input, expected):
    correct_password = test_input["correct_password"]
    input_password = test_input["input_password"]
    hashed_password = auth_modules.get_password_hash(correct_password)
    
    is_verified = auth_modules.verify_password(input_password, hashed_password)
    
    assert is_verified == expected, "Password verification failed"

@pytest.mark.asyncio
async def test_create_user_CreateUser_ReturnUser(db_session: AsyncSession):
    user_name = "test_user"
    new_user = await auth_modules.create_user(db_session, user_name)
    assert new_user.name == user_name, "failed at create_user"
    
@pytest.mark.asyncio
async def test_get_user_GetUserInfo_ReturnUser(db_session: AsyncSession, mocker):
    user_name = "test_user"
    test_user = User(id=1, name=user_name)
    mocker.patch.object(db_session, 'scalar', return_value=test_user)
    fetched_user = await auth_modules.get_user(db_session, user_name)
    assert fetched_user.name == user_name, "User name does not match"

@pytest.mark.asyncio
async def test_create_password_CreatePassword_ReturnHashedPassword(db_session: AsyncSession):
    user_name = "test_user"
    await auth_modules.create_user(db_session, user_name)
    fetched_user = await auth_modules.get_user(db_session, user_name)
    password_body = auth_schemes.PasswordCreate(user_id=fetched_user.id, password="test_password")
    
    new_password = await auth_modules.create_password(db_session, password_body)
    
    assert new_password is not None, "failed at create_password"

@pytest.mark.asyncio
async def test_get_password_GetUserPassword_ReturnPassword(db_session: AsyncSession, mocker):
    test_hashed_password = "test_password"
    mocker.patch.object(db_session, 'scalar', return_value=Password(user_id=1, password=test_hashed_password))
    hashed_password = await auth_modules.get_password(db_session, 1)
    assert hashed_password is not None, "failed at get_password"
    
@pytest.mark.asyncio
async def test_authenticate_user_AuthenticateSingleUser_ReturnUser(db_session: AsyncSession, mocker):
    user_name = "test_user"
    user_password = "test_password"
    mocker.patch("repository.auth.user.get_user", return_value=User(id=1, name=user_name))
    mocker.patch("repository.auth.user.get_password", return_value=Password(user_id=1, password=user_password))
    mocker.patch("repository.auth.user.verify_password", return_value=True)
    
    is_authenticated = await auth_modules.authenticate_user(db_session, user_name, user_password)
    
    assert is_authenticated is not False, "failed at authenticate_user"

@pytest.mark.asyncio
async def test_authenticate_user_AuthenticateSingleUserWithWrongPassword_ReturnFalse(db_session: AsyncSession, mocker):
    user_name = "test_user"
    user_password = "wrong_password"
    mocker.patch("repository.auth.user.get_user", return_value=User(id=1, name=user_name))
    mocker.patch("repository.auth.user.get_password", return_value=Password(user_id=1, password="test_password"))
    mocker.patch("repository.auth.user.verify_password", return_value=False)
    
    is_authenticated = await auth_modules.authenticate_user(db_session, user_name, user_password)
    
    assert is_authenticated is False, "failed at authenticate_user"

def test_create_access_token_CreateAccessToken_ReturnAccessToken():
    user_id = 1
    token = auth_modules.create_access_token(data={"sub": str(user_id)})
    assert token, "The access token should not be empty."
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") ==  str(user_id), "The token payload should contain the correct user ID."
    
async def test_get_current_user_id_GetUserIDFromAccessToken_ReturnUserID(db_session: AsyncSession):
    token = auth_modules.create_access_token(data={"sub": "1"})
    user_id = await auth_modules.get_current_user_id(db_session, token=token)
    assert user_id == "1", "The user ID should be extracted from the token."