import factory
from apps.user.models import CustomUser

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    
    email = factory.Faker('email')
    password = factory.Faker('password')