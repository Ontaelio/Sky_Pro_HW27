import json

import pytest

from ads.serializers import AdDetailSerializer
from tests.factories import *


@pytest.mark.django_db
def test_ad_list(client):
    ads = AdFactory.create_batch(10, category=CategoryFactory(name='foo'))

    result = client.get("/ad/")

    # keeping these for future checks in case evil stuff starts happening
    # print(dir(result))
    # print(result.content)
    # print(json.loads(result.content)['items'][0])

    assert result.status_code == 200
    response = json.loads(result.content)
    assert response["items"][1]["category"] == ads[1].category.name
    assert len(response["items"]) == 10
    assert response["num_pages"] == 1
    assert response["total"] == 10


@pytest.mark.django_db
def test_create(client, ad, user, category):

    expected_response = {
        "id": ad.pk + 1,
        "name": ad.name,
        "author_id": user.pk,
        "author": user.username,
        "price": str(ad.price),
        "description": "",
        "is_published": False,
        "category_id": category.pk,
        "category": category.name,
        "image": None,
        "tags": [],
        "location": user.location.name
    }

    response = client.post(
        '/ad/',
        {
            "name": ad.name,
            "author_id": user.id,
            "category_id": category.pk,
            "price": ad.price
        },
        content_type="application/json",
        # format='json',
    )

    assert response.status_code == 200
    assert json.loads(response.content) == expected_response


def test_error():
    ...
