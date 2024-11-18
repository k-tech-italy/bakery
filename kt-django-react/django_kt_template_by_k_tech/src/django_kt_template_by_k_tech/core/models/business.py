from django.core.exceptions import ValidationError
from django.db import models

from django_kt_template_by_k_tech.core.models.common import Auditable
from django_kt_template_by_k_tech.core.models.dimensions import ExampleDimension1


class ExampleBusiness1(Auditable):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

