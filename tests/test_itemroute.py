from config import setting

def test_create_item(client):
    response = client.post(
        "/items/create/",
        json={ "title": setting.TITLE, "description": setting.DESCRIPTION}
    )
    assert response.status_code == 202

def test_retrieve_by_id(client):
    response = client.get("/items/1")
    print(response)
    assert response.status_code == 202
    assert response.json()['title'] == setting.TITLE
    assert response.json()['description'] == setting.DESCRIPTION