import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_replies(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    post_response = await async_client.post("/post", json={"text": "Parent post"}, cookies={"access_token": access_token})
    parent_post_id = post_response.json()["new_post"]["id"]

    response = await async_client.get(f"/replies/{parent_post_id}")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_post_reply(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    post_response = await async_client.post("/post", json={"text": "Parent post"}, cookies={"access_token": access_token})
    parent_post_id = post_response.json()["new_post"]["id"]

    reply_text = "This is a reply."
    response = await async_client.post(f"/reply/{parent_post_id}", json={"text": reply_text}, cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully created reply."

    response = await async_client.get(f"/replies/{parent_post_id}")
    assert response.status_code == 200
    replies = response.json()
    assert len(replies) == 1
    assert replies[0]["text"] == reply_text

@pytest.mark.asyncio
async def test_delete_reply(async_client: AsyncClient):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    post_response = await async_client.post("/post", json={"text": "Parent post"}, cookies={"access_token": access_token})
    parent_post_id = post_response.json()["new_post"]["id"]

    reply_text = "This is a reply."
    reply_response = await async_client.post(f"/reply/{parent_post_id}", json={"text": reply_text}, cookies={"access_token": access_token})
    reply_id = reply_response.json()["new_reply"]["id"]

    response = await async_client.delete(f"/reply/{reply_id}", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully deleted reply."}

    response = await async_client.get(f"/replies/{parent_post_id}")
    assert response.status_code == 200
    replies = response.json()
    assert len(replies) == 0
