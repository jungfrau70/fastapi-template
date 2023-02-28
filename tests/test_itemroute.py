def test_create_item(client, header_token): 
    response = client.post(
        "/items/create/",
        json={ "title": "Item100", "description": "This is item100"},
        headers = header_token
    )
    assert response.status_code == 202

def test_retrieve_item_by_id(client):
    response = client.get("/items/1")
    # print(response)
    assert response.status_code == 202
    assert response.json()['title'] == "Item100"
    assert response.json()['description'] == "This is item100"