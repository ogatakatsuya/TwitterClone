import pytest

@pytest.mark.asyncio
async def test_create_post_with_valid_token(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    response = await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )
    assert response.status_code == 200
    assert "new_post" in response.json()

@pytest.mark.asyncio
async def test_create_post_without_token(async_client):
    response = await async_client.post("/post", json={"text": "This is a test post"})
    assert response.status_code == 401
    assert response.json() == {"detail": "アクセストークンが見つかりません．再度ログインしてください．"}

@pytest.mark.asyncio
async def test_get_posts(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )

    response = await async_client.get("/posts", params={"offset": 0, "limit": 10})
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_post(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    create_response = await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )
    post_id = create_response.json()["new_post"]["id"]

    response = await async_client.get(f"/post/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id

@pytest.mark.asyncio
async def test_delete_post(async_client):
    await async_client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    login_response = await async_client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.cookies.get("access_token")

    create_response = await async_client.post(
        "/post",
        json={"text": "This is a test post"},
        cookies={"access_token": access_token}
    )
    post_id = create_response.json()["new_post"]["id"]

    response = await async_client.delete(f"/post/{post_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Post deleted"}
