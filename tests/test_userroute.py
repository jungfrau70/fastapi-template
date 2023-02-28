from config import setting

def test_create_user(client):
    response = client.post(
        "/users/create/",
        json={ "email": "user2@example.com", "name": "User2", "password" : "user2"}
    )
    assert response.status_code == 202
    assert response.json()["email"] == "user2@example.com"
    assert response.json()["is_active"] == True