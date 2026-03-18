"""API tests for JSONPlaceholder posts endpoints."""

from __future__ import annotations

import pytest

from src.api.api_client import APIClient


@pytest.mark.api
def test_get_posts_status_and_size(api_client: APIClient) -> None:
    response = api_client.get("/posts")
    assert response.status_code == 200

    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100


@pytest.mark.api
def test_get_post_by_id_validates_fields(api_client: APIClient) -> None:
    response = api_client.get("/posts/1")
    assert response.status_code == 200

    post = response.json()
    assert post["id"] == 1
    assert isinstance(post["title"], str)
    assert post["title"].strip() != ""


@pytest.mark.api
def test_create_post(api_client: APIClient) -> None:
    payload = {
        "title": "automation framework",
        "body": "post created by API test",
        "userId": 1,
    }
    response = api_client.post("/posts", json=payload)
    assert response.status_code == 201

    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert "id" in created


@pytest.mark.api
def test_update_post(api_client: APIClient) -> None:
    payload = {
        "id": 1,
        "title": "updated title",
        "body": "updated body",
        "userId": 1,
    }
    response = api_client.put("/posts/1", json=payload)
    assert response.status_code == 200

    updated = response.json()
    assert updated["id"] == 1
    assert updated["title"] == payload["title"]
    assert updated["body"] == payload["body"]


@pytest.mark.api
def test_delete_post(api_client: APIClient) -> None:
    response = api_client.delete("/posts/1")
    assert response.status_code == 200
