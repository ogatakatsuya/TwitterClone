import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_my_following_users(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    response = await async_client.get("/follow", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == 0

@pytest.mark.asyncio
async def test_get_users_following_me(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    response = await async_client.get("/followed", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == 0

@pytest.mark.asyncio
async def test_follow_user(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "user1", "password": "password1"})
    await async_client.post("/auth/register", json={"user_name": "user2", "password": "password2"})
    
    login_response_user1 = await async_client.post("/auth/login", data={"username": "user1", "password": "password1"})
    login_response_user2 = await async_client.post("/auth/login", data={"username": "user2", "password": "password2"})
    access_token_user1 = login_response_user1.cookies.get("access_token")
    access_token_user2 = login_response_user2.cookies.get("access_token")
    
    user2_id_response = await async_client.get("/user", cookies={"access_token": access_token_user2})
    user2_id = user2_id_response.json()

    # User1 follows User2
    response = await async_client.post(f"/follow/{user2_id}", cookies={"access_token": access_token_user1})
    assert response.status_code == 200
    assert response.json() == {"message": "successfully followed"}

@pytest.mark.asyncio
async def test_remove_follow(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "user1", "password": "password1"})
    await async_client.post("/auth/register", json={"user_name": "user2", "password": "password2"})
    
    login_response_user1 = await async_client.post("/auth/login", data={"username": "user1", "password": "password1"})
    login_response_user2 = await async_client.post("/auth/login", data={"username": "user2", "password": "password2"})
    access_token_user1 = login_response_user1.cookies.get("access_token")
    access_token_user2 = login_response_user2.cookies.get("access_token")
    
    user2_id_response = await async_client.get("/user", cookies={"access_token": access_token_user2})
    user2_id = user2_id_response.json()

    # User1 follows User2
    await async_client.post(f"/follow/{user2_id}", cookies={"access_token": access_token_user1})

    # User1 unfollows User2
    response = await async_client.delete(f"/follow/{user2_id}", cookies={"access_token": access_token_user1})
    assert response.status_code == 200
    assert response.json() == {"message": "successfully delete"}

@pytest.mark.asyncio
async def test_get_users_following(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "user1", "password": "password1"})
    await async_client.post("/auth/register", json={"user_name": "user2", "password": "password2"})
    
    login_response_user1 = await async_client.post("/auth/login", data={"username": "user1", "password": "password1"})
    login_response_user2 = await async_client.post("/auth/login", data={"username": "user2", "password": "password2"})
    access_token_user1 = login_response_user1.cookies.get("access_token")
    access_token_user2 = login_response_user2.cookies.get("access_token")
    
    user2_id_response = await async_client.get("/user", cookies={"access_token": access_token_user2})
    user2_id = user2_id_response.json()

    # User1 follows User2
    await async_client.post(f"/follow/{user2_id}", cookies={"access_token": access_token_user1})

    # Get the number of users User2 is following
    response = await async_client.get(f"/follow/{user2_id}")
    assert response.status_code == 200
    assert response.json() == 1

@pytest.mark.asyncio
async def test_get_users_followed(async_client: AsyncClient):
    # Register and login two users
    await async_client.post("/auth/register", json={"user_name": "user1", "password": "password1"})
    await async_client.post("/auth/register", json={"user_name": "user2", "password": "password2"})
    
    login_response_user1 = await async_client.post("/auth/login", data={"username": "user1", "password": "password1"})
    login_response_user2 = await async_client.post("/auth/login", data={"username": "user2", "password": "password2"})
    access_token_user1 = login_response_user1.cookies.get("access_token")
    access_token_user2 = login_response_user2.cookies.get("access_token")
    
    user2_id_response = await async_client.get("/user", cookies={"access_token": access_token_user2})
    user2_id = user2_id_response.json()

    # User1 follows User2
    await async_client.post(f"/follow/{user2_id}", cookies={"access_token": access_token_user1})

    # Get the number of users following User2
    response = await async_client.get(f"/followed/{user2_id}")
    assert response.status_code == 200
    assert response.json() == 1

@pytest.mark.asyncio
async def test_find_follow(async_client: AsyncClient):
    # Register and login two users
    await async_client.post("/auth/register", json={"user_name": "user1", "password": "password1"})
    await async_client.post("/auth/register", json={"user_name": "user2", "password": "password2"})
    
    login_response_user1 = await async_client.post("/auth/login", data={"username": "user1", "password": "password1"})
    login_response_user2 = await async_client.post("/auth/login", data={"username": "user2", "password": "password2"})
    access_token_user1 = login_response_user1.cookies.get("access_token")
    access_token_user2 = login_response_user2.cookies.get("access_token")
    
    user2_id_response = await async_client.get("/user", cookies={"access_token": access_token_user2})
    user2_id = user2_id_response.json()

    # User1 follows User2
    await async_client.post(f"/follow/{user2_id}", cookies={"access_token": access_token_user1})

    # Check if User1 follows User2
    response = await async_client.get(f"/isfollow/{user2_id}", cookies={"access_token": access_token_user1})
    assert response.status_code == 200
    assert response.json() is True

