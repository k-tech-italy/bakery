from django.dispatch import Signal

from {{cookiecutter.project__module}}_version_upgraded = Signal(providing_args=['version'])
cli_{{cookiecutter.project__module}}_upgrade_templates = Signal(providing_args=['verbosity', 'context'])
cli_{{cookiecutter.project__module}}_execute_command = Signal(providing_args=['context' ])
