from pytest_factoryboy import register

from tests.factories import *


# Factories
register(LocationFactory)
register(UserFactory)
# register(RandomUserFactory)
register(TagFactory)
register(CategoryFactory)
# register(RandomAdFactory)
register(AdFactory)


