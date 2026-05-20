import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user%02d" % n)
    email = factory.Sequence(lambda n: "u%02d@example.com" % n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = True

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        super()._after_postgeneration(instance, create, results)
        if create:
            instance.save()
        instance._raw_password = "password"  # noqa: S105

    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)
        skip_postgeneration_save = True
