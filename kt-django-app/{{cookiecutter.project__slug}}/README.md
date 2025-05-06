# {{ cookiecutter.project__name }}

<!--
[![Test]({{ cookiecutter.__github_base_url }}/actions/workflows/test.yml/badge.svg)]({{ cookiecutter.__github_base_url }}/actions/workflows/test.yml)
[![Lint]({{ cookiecutter.__github_base_url }}/actions/workflows/lint.yml/badge.svg)]({{ cookiecutter.__github_base_url }}/actions/workflows/lint.yml)
[![Documentation]({{ cookiecutter.__github_base_url }}/actions/workflows/docs.yml/badge.svg)]({{ cookiecutter.__github_base_url }}/actions/workflows/docs.yml)
[![codecov](https://codecov.io/github/{{ cookiecutter.github_team }}/{{ cookiecutter.project__slug }}/graph/badge.svg?token=BNXEW4JAYF)](https://codecov.io/github/{{ cookiecutter.github_team }}/{{ cookiecutter.project__slug }})
-->


{{ cookiecutter.project__name }} is a Django app.

NOTE: Provide a more detailed description here.


## Dependencies

* Python 3.9 or later
* Django 4.2 or later


## Installation

* Install {{ cookiecutter.project__slug }} using your package manager of choice, e.g. Pip:
  ```bash
  pip install {{ cookiecutter.project__slug }}
  ```

* Add {{ cookiecutter.project__slug }} to `INSTALLED_APPS` in your `config/settings.py` file:
  ```python
  INSTALLED_APPS = (
      ...
      "{{ cookiecutter.project__slug }}",
      ...
  )
  ```

* Check that your configuration is valid:
  ```bash
  python manage.py check
  ```

## Bug reports and requests for enhancements

Please open an issue on the project's [issue tracker on GitHub]({{ cookiecutter.__github_base_url }}/issues).

## Contributing to the project

See the [contribution guide](CONTRIBUTING.md).

## Licensing

All rights reserved.
