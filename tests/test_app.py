import pytest
from httpx import AsyncClient
from fastapi import status
from src.app import app

import pytest

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_for_activity():
    test_email = "testuser@mergington.edu"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Ensure not already signed up
        await ac.post(f"/activities/Chess%20Club/signup?email=remove_{test_email}")
        response = await ac.post(f"/activities/Chess%20Club/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email} for Chess Club" in response.text

@pytest.mark.asyncio
async def test_signup_duplicate():
    test_email = "duplicate@mergington.edu"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(f"/activities/Programming%20Class/signup?email={test_email}")
        response = await ac.post(f"/activities/Programming%20Class/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.text

@pytest.mark.asyncio
async def test_signup_activity_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.text
