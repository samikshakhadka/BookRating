import factory
from apps.user.models import CustomUser

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    
    email = factory.Faker('email')
    #password = factory.Faker('password')

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('defaultpassword')