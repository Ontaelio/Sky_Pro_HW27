import json

import pytest

from ads.models import Ad, Category
from authentication.models import User, Location


@pytest.mark.django_db
def test_s(client):
    location = Location.objects.create(
        name="Ivanovo"
    )

    user = User.objects.create(
        username="testuser",
        password="123",
        birth_date="1970-10-10",
        location=location
    )

    category = Category.objects.create(
        slug="123456",
        name="foo_and_bar_100"
    )

    ad = Ad.objects.create(
        name="test test test",
        price=205,
        author=user,
        category=category
    )

    result = client.get("/ad/")

    assert result.status_code == 200
    # print(dir(result)) #.content
    # print(result.content)
    # print(json.loads(result.content))

    assert float(json.loads(result.content)["items"][0]["price"]) == 205.00
