import logging

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import site

import {{cookiecutter.project__slug}}

site.site_title = '{{cookiecutter.project__name}}'
site.site_header = '{{cookiecutter.project__name}} admin console ' + {{cookiecutter.project__slug}}.__version__
site.enable_nav_sidebar = True


logger = logging.getLogger(__name__)


