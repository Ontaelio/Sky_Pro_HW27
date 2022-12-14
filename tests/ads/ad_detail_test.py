import json

import pytest

from ads.views import ad_as_dict
from tests.factories import *


@pytest.mark.django_db
def test_ad_details_no_auth(client):
    ads = AdFactory.create_batch(5)
    result = client.get(f"/ad/{ads[0].pk}/")
    assert result.status_code == 401


@pytest.mark.django_db
def test_ad_details(client, new_user_and_token):
    ads = AdFactory.create_batch(5)
    result = client.get(f"/ad/{ads[4].pk}/",
                        HTTP_AUTHORIZATION="Bearer " + new_user_and_token["tokens"]["access"])
    response = json.loads(result.content)
    assert result.status_code == 200
    assert ad_as_dict(ads[4]) == response


@pytest.mark.django_db
def test_ad_details_nonexistant(client, new_user_and_token):
    ad = AdFactory()
    result = client.get(f"/ad/{ad.pk + 2000}/",
                        HTTP_AUTHORIZATION="Bearer " + new_user_and_token["tokens"]["access"])
    assert result.status_code == 404

