import pytest

from tests.factories import *


@pytest.mark.django_db
def test_create(client, new_user_and_token):
    ads = AdFactory.create_batch(10)

    selection_data = {
        "name": "test selection",
        "owner": new_user_and_token["user"]["id"],
        "items": [ads[0].pk, ads[3].pk, ads[7].pk]
    }

    expected_response = {
        "id": 'unknown_yet',
        "name": "test selection",
        "items": selection_data["items"]
    }

    response = client.post(
        '/selection/create/',
        selection_data,
        content_type="application/json",
    )

    assert response.status_code == 401

    response = client.post(
        '/selection/create/',
        selection_data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + new_user_and_token["tokens"]["access"]
    )

    assert response.status_code == 201
    expected_response["id"] = response.data["id"]
    assert response.data == expected_response
