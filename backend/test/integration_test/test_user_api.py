import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_own_profile_information(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    response = await async_client.get("/profile", cookies={"access_token": access_token})
    assert response.status_code == 200
    profile = response.json()
    profile["id"] = 1

@pytest.mark.asyncio
async def test_edit_own_profile_information(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    new_profile_data = {
        "nickname": "new_nickname",
        "biography": "new_biography",
        "birth_day": "2000-01-01"
    }
    response = await async_client.put("/profile", json=new_profile_data, cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully edit profile"}

    response = await async_client.get("/profile", cookies={"access_token": access_token})
    assert response.status_code == 200
    profile = response.json()
    assert profile["nickname"] == "new_nickname"
    assert profile["biography"] == "new_biography"
    assert profile["birth_day"] == "2000-01-01T00:00:00"

@pytest.mark.asyncio
async def test_get_own_posts(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    await async_client.post("/post", json={"text": "My post"}, cookies={"access_token": access_token})

    response = await async_client.get("/profile/post?offset=0", cookies={"access_token": access_token})
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["text"] == "My post"

@pytest.mark.asyncio
async def test_get_personal_posts(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    await async_client.post("/post", json={"text": "My post"}, cookies={"access_token": access_token})

    response = await async_client.get("/profile/post/1?offset=0")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["text"] == "My post"

@pytest.mark.asyncio
async def test_get_profile_information(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    # Retrieve profile information by user_id
    response = await async_client.get("/profile/1")
    assert response.status_code == 200
    profile = response.json()
    assert profile["id"] == 1  # Assuming the user_id is 1

@pytest.mark.asyncio
async def test_edit_profile_information(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    new_profile_data = {
        "nickname": "new_nickname",
        "biography": "new_biography",
        "birth_day": "2000-01-01"
    }
    response = await async_client.put("/profile/1", json=new_profile_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully edit profile"}

    response = await async_client.get("/profile/1")
    assert response.status_code == 200
    profile = response.json()
    assert profile["nickname"] == "new_nickname"
    assert profile["biography"] == "new_biography"
    assert profile["birth_day"] == "2000-01-01T00:00:00"
