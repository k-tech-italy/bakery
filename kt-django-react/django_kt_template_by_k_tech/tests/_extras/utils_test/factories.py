import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda o: f'email{o}@example.com')
    username = factory.LazyAttribute(lambda o: o.email)
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')

    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.user_permissions.add(*extracted)
