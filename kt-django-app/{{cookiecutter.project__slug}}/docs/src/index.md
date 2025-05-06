---
title: Documentation
---

{{ cookiecutter.project__name }} is a Django app.

TODO: Provide a more detailed description here.


## Dependencies

* Python 3.9 or later
* Django 4.2 or any later version supporting your Python version of choice.


## Installation

* Install {{ cookiecutter.project__slug }} using your package manager of choice, e.g. Pip:
  ```bash
  pip install {{ cookiecutter.project__slug }}
  ```

* Add `{{ cookiecutter.project__slug }}` to `INSTALLED_APPS` in your `config/settings.py` file:
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

See the [contribution guide](contributing.md).

## Licensing

All rights reserved.
