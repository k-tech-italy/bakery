import os

import djclick as click
from django.contrib.auth.models import User

from django_kt_template_by_k_tech.config.environ import env


@click.group()
def group():
    """ Manages demo setup """


@group.command()
def setup():
    """ Setup initial data """
    if User.objects.count() == 0:
        User.objects.create_superuser(username=env('ADMIN_USERNAME'),
                                      email=env('ADMIN_EMAIL'),
                                      password=env('ADMIN_PASSWORD'))
