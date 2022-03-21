class {{cookiecutter.project__title}}Error(Exception):
    default_message = 'Error'

    def __init__(self, message=None, **kwargs):
        self.message = str(message) or self.default_message
        self.extra = kwargs


class ImproperlyConfigured({{cookiecutter.project__title}}Error):
    pass
