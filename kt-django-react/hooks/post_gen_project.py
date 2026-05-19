import os
import shutil

USE_CELERY = "{{ cookiecutter.use_celery }}" == "yes"
USE_MKDOCS = "{{ cookiecutter.use_mkdocs }}" == "yes"
USE_TRIVY = "{{ cookiecutter.use_trivy }}" == "yes"
LICENSE = "{{ cookiecutter.open_source_license }}"
PKG = "{{ cookiecutter.package_name }}"


def remove(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


if not USE_CELERY:
    remove(f"src/{PKG}/config/celery.py")
    remove("tests/_extras/test_utils/celery.py")

if not USE_MKDOCS:
    remove("docs")
    remove("mkdocs.yml")
    remove(".github/workflows/docs.yml")

if not USE_TRIVY:
    remove(".trivyignore")

if LICENSE == "none":
    remove("LICENSE")

print("\n  Project '{{ cookiecutter.project_name }}' created. See CONTRIBUTING.md to get started.\n")