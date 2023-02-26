import os
import sys
import json

def test_create_user(client):
    response = client.post(
        "/users/create/",
        headers={"X-Token": "hailhydra"},
        json={ "email": "testuser1@test.com", "name": "TestUser1", "password" : "testuser1"}
    )
    assert response.status_code == 202
    assert response.json()["email"] == "testuser1@test.com"
    assert response.json()["is_active"] == True