import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_likes_num(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    post_response = await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )
    post_id = post_response.json()["new_post"]["id"]

    response = await async_client.get(f"/likes/{post_id}", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json()["like_num"] == 0
    assert response.json()["is_like"] is False

@pytest.mark.asyncio
async def test_post_like(async_client: AsyncClient):
    # Register and login to get an access token and create a post
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    # Create a post
    post_response = await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )
    post_id = post_response.json()["new_post"]["id"]

    response = await async_client.post(f"/like/{post_id}", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == {"message": "successfully like created."}

    likes_response = await async_client.get(f"/likes/{post_id}", cookies={"access_token": access_token})
    assert likes_response.status_code == 200
    assert likes_response.json()["like_num"] == 1
    assert likes_response.json()["is_like"] is True

@pytest.mark.asyncio
async def test_remove_like(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    post_response = await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )
    post_id = post_response.json()["new_post"]["id"]

    await async_client.post(f"/like/{post_id}", cookies={"access_token": access_token})

    response = await async_client.delete(f"/like/{post_id}", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == {"message": "successfully deleted like."}

    likes_response = await async_client.get(f"/likes/{post_id}", cookies={"access_token": access_token})
    assert likes_response.status_code == 200
    assert likes_response.json()["like_num"] == 0
    assert likes_response.json()["is_like"] is False
