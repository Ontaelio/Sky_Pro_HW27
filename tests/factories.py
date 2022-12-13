import factory.django
import faker.providers.internet.en_US

from ads.models import Tag, Category, Ad
from authentication.models import Location, User


#factory.Faker.add_provider(faker.providers.address.)

# class LocationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Location
#
#     name = "Тестовый проезд, д. 1"


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Faker('address', locale='ru_RU')


# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User
#
#     username = "test"
#     password = "12345"
#     birth_date = "1970-10-10"
#     location = factory.SubFactory(LocationFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('ascii_email')
    birth_date = factory.Faker('date_of_birth', minimum_age=8) #"1970-10-10"
    location = factory.SubFactory(LocationFactory)
    role = "member"


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = "test"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    slug = factory.Faker('pystr', min_chars=5, max_chars=10)
    name = factory.Faker('sentence', nb_words=3)


# class AdFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Ad
#
#     name = "A vey beautiful testing object"
#     author = factory.SubFactory(UserFactory)
#     category = factory.SubFactory(CategoryFactory)
#     price = 2000


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker('text', locale='ru_RU', max_nb_chars=100)
    description = factory.Faker('text', locale='ru_RU', max_nb_chars=2000)
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    price = factory.Faker('pydecimal', right_digits=2, positive=True, max_value=200000)
    is_published = False
    # tags = factory.SubFactory(TagFactory)
    image = None

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)





