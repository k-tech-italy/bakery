import logging

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import site

import django_kt_template_by_k_tech

site.site_title = 'Django KT template by K-Tech'
site.site_header = 'Django KT template by K-Tech admin console ' + django_kt_template_by_k_tech.__version__
site.enable_nav_sidebar = True


logger = logging.getLogger(__name__)


