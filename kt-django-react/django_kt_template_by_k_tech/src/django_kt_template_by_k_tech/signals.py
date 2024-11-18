from django.dispatch import Signal

django_kt_template_by_k_tech_version_upgraded = Signal(providing_args=['version'])
cli_django_kt_template_by_k_tech_upgrade_templates = Signal(providing_args=['verbosity', 'context'])
cli_django_kt_template_by_k_tech_execute_command = Signal(providing_args=['context', ])
