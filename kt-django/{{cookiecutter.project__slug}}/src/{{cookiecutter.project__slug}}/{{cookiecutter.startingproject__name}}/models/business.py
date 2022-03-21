from django.core.exceptions import ValidationError
from django.db import models

from {{cookiecutter.project__slug}}.{{cookiecutter.startingproject__name}}.models.common import Auditable
from {{cookiecutter.project__slug}}.{{cookiecutter.startingproject__name}}.models.dimensions import ExampleDimension1


class ExampleBusiness1(Auditable):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

