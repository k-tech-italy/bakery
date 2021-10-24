from django.dispatch import Signal

{{cookiecutter.project__slug}}_version_upgraded = Signal(providing_args=['version'])
cli_{{cookiecutter.project__slug}}_upgrade_templates = Signal(providing_args=['verbosity', 'context'])
cli_{{cookiecutter.project__slug}}_execute_command = Signal(providing_args=['context', ])
