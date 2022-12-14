import json

import pytest

from ads.views import ad_as_dict
from tests.factories import *


@pytest.mark.django_db
def test_ad_list(client):
    ads = AdFactory.create_batch(10)

    result = client.get("/ad/")

    # keeping these for future checks in case evil stuff starts happening
    # reminder: pytest -s for print to work
    # print(dir(result))
    # print(result.content)
    # print(json.loads(result.content)['items'][0])

    assert result.status_code == 200
    response = json.loads(result.content)
    assert response["num_pages"] == 1
    assert response["total"] == 10

    for ad in ads:
        assert ad_as_dict(ad) in response["items"]

