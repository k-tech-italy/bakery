import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from {{cookiecutter.project__slug}}.{{cookiecutter.startingproject__name}}.models import (
        ExampleBusiness1, ExampleDimension1
    )


logger = logging.getLogger(__name__)


@admin.register(ExampleBusiness1)
class ExampleBusiness1Admin(ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(ExampleDimension1)
class ExampleDimension1Admin(ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
