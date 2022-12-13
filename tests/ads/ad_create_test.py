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
def test_create(client, user, category):
    ad_data = {
        "name": "test ad name",
        "author_id": user.pk,
        "price": "2005.12",
        "category_id": category.pk,
        "description": faker.Faker(locale='ru_RU').text(max_nb_chars=2000),
        "tags": ["tag1", "tag2", "robots"]
    }

    expected_response = {
        "id": 'unknown_yet',
        "name": ad_data['name'],
        "author_id": user.pk,
        "author": user.username,
        "price": str(ad_data["price"]),
        "description": ad_data["description"],
        "is_published": False,
        "category_id": category.pk,
        "category": category.name,
        "image": None,
        "tags": ad_data["tags"],
        "location": user.location.name
    }

    response = client.post(
        '/ad/',
        ad_data,
        content_type="application/json",
        # format='json',
    )

    expected_response["id"] = json.loads(response.content)["id"]

    assert response.status_code == 200
    assert json.loads(response.content) == expected_response


@pytest.mark.parametrize('field', ["name", "author_id", "category_id", "price"])
@pytest.mark.django_db
def test_missing_data(client, ad, field):
    data = {
        "name": ad.name,
        "author_id": ad.author.id,
        "category_id": ad.category.pk,
        "price": ad.price,
    }
    del data[field]
    response = client.post(
        '/ad/',
        data,
        content_type="application/json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_published_false(client, ad):
    data = {
        "name": ad.name,
        "author_id": ad.author.id,
        "category_id": ad.category.pk,
        "price": ad.price,
        "is_published": True
    }

    response = client.post(
        '/ad/',
        data,
        content_type="application/json",
    )

    assert json.loads(response.content)["is_published"] is False


@pytest.mark.parametrize('names,code', [("four", 422), ("NineChars", 422), ("TenChrctrs", 200)])
@pytest.mark.django_db
def test_name_length(client, ad, names, code):
    data = {
        "name": names,
        "author_id": ad.author.id,
        "category_id": ad.category.pk,
        "price": ad.price,
        "is_published": True
    }

    response = client.post(
        '/ad/',
        data,
        content_type="application/json",
    )

    assert response.status_code == code
