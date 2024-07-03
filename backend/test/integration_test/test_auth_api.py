import pytest

@pytest.mark.asyncio
async def test_register_new_account_ResisterUser_ReturnSuccessMessage(async_client):
        response = await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
        assert response.status_code == 200
        assert response.json() == {"message": "user created."}

@pytest.mark.asyncio
async def test_login_for_access_token_LoginWithValidCredentials_ReturnsAccessToken(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.cookies

@pytest.mark.asyncio
async def test_login_for_access_token_LoginWithInvalidCredentials_ReturnsUnauthorized(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    response = await async_client.post("/auth/login", data={"username": "test_user", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

@pytest.mark.asyncio
async def test_logout_user_LogoutUser_RemovesAccessToken(async_client):
    # まずユーザーを登録してログイン
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    response = await async_client.delete("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully log out"}
    assert "access_token" not in response.cookies

@pytest.mark.asyncio
async def test_get_user_id_GetUserIdWithValidToken_ReturnsUserId(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")
    response = await async_client.get("/user", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json().isdigit()

@pytest.mark.asyncio
async def test_get_user_id_GetUserIdWithInvalidToken_ReturnsUnauthorized(async_client):
    response = await async_client.get("/user", cookies={"access_token": "invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "再度ログインしてください．"}
