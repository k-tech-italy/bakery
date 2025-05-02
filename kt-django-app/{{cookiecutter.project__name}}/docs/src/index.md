---
title: Documentation
---

{{ cookiecutter.project__name }} is 

- extend configuration
- management command
- django check framework integration


## Install

    pip install {{ cookiecutter.project__slug }}


In your `settings.py`:
    
    INSTALLED_APPS = [
        ...
        "{{ cookiecutter.project__module }}"
    ]

Check your configuration

    python manage.py check

