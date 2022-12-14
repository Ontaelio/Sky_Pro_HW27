import faker
import pytest


@pytest.fixture
@pytest.mark.django_db
def new_user_and_token(client):
    user_data = {
        "username": faker.Faker().user_name(),
        "password": faker.Faker().password(),
        "email": faker.Faker().ascii_email(),
        "birth_date": faker.Faker().date_of_birth(minimum_age=8),
    }

    user = client.post(
            '/user/create/',
            user_data,
            content_type="application/json"
        ).data

    tokens = client.post(
        '/user/token/',
        user_data,
        content_type="application/json"
    ).data

    return {"user": user, "tokens": tokens}
