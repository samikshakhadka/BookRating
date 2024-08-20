import factory
from factory.django import DjangoModelFactory
from apps.user.models import CustomUser
from apps.book.models import Book, Favorite
from apps.user.tests.factories import UserFactory

# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = CustomUser

#     email = factory.Faker('email')
#     first_name = factory.Faker('first_name')
#     last_name = factory.Faker('last_name')
#     is_verified = True

#     @factory.post_generation
#     def password(self, create, extracted, **kwargs):
#         if not create:
#             return

#         if extracted:
#             self.set_password(extracted)
#         else:
#             self.set_password('password123')


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author = factory.Faker('name')
    description = factory.Faker('paragraph')
    created_by = factory.SubFactory(UserFactory)

    

class FavoriteFactory(DjangoModelFactory):
    class Meta:
        model = Favorite

    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory)
