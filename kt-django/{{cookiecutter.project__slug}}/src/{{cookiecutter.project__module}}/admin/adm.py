import logging

from django.contrib.admin.sites import site
from {{cookiecutter.project__module}} import __version__

site.site_title = "{{cookiecutter.project__name}}"
site.site_header = "{{cookiecutter.project__name}} admin console " + __version__
site.enable_nav_sidebar = True


logger = logging.getLogger(__name__)
