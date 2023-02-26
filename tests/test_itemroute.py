import os
import sys
import json

def test_create_item(client):
    response = client.post(
        "/items/create/",
        headers={"X-Token": "hailhydra"},
        json={ "title": "Item1", "description": "This is Item1"}
    )
    assert response.status_code == 202

def test_retrieve_by_id(client):
    response = client.get(
        "/items/1",
        headers={"X-Token": "hailhydra"},
    )
    assert response.status_code == 202
    assert response.json()['title'] == "Item1"
    assert response.json()['description'] == "This is Item1"