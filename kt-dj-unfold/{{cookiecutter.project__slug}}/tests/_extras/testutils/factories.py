from datetime import date, timedelta

import factory
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from factory import PostGenerationMethodCall
from factory.base import FactoryMetaClass
from factory.fuzzy import FuzzyDecimal

from {{cookiecutter.project_module}}.config import settings
from {{cookiecutter.project_module}}.core.models import User
from {{cookiecutter.project_module}}.currencies.models import Currency

factories_registry = {}


class AutoRegisterFactoryMetaClass(FactoryMetaClass):
    def __new__(cls, class_name, bases, attrs):
        new_class = super().__new__(cls, class_name, bases, attrs)
        factories_registry[new_class._meta.model] = new_class
        return new_class


class AutoRegisterModelFactory(factory.django.DjangoModelFactory, metaclass=AutoRegisterFactoryMetaClass):
    pass


def get_factory_for_model(_model):
    class Meta:
        model = _model

    if _model in factories_registry:
        return factories_registry[_model]
    return type(f'{_model._meta.model_name}AutoFactory', (AutoRegisterModelFactory,), {'Meta': Meta})


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'User %02d' % n)
    email = factory.Sequence(lambda n: 'u%02d@example.com' % n)
    first_name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        super()._after_postgeneration(instance, create, results)
        instance._password = 'password'

    class Meta:
        model = User
        django_get_or_create = ('username',)


class SuperUserFactory(UserFactory):
    username = factory.Sequence(lambda n: 'superuser%03d@example.com' % n)
    email = factory.Sequence(lambda n: 'superuser%03d@example.com' % n)
    is_superuser = True
    is_staff = True
    is_active = True


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Group %02d' % n)

    class Meta:
        model = Group
        django_get_or_create = ('name',)

