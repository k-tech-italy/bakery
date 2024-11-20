import logging

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import site

import {{ cookiecutter.project__module }}

site.site_title = 'Django KT template by K-Tech'
site.site_header = 'Django KT template by K-Tech admin console ' + {{ cookiecutter.project__module }}.__version__
site.enable_nav_sidebar = True


logger = logging.getLogger(__name__)


