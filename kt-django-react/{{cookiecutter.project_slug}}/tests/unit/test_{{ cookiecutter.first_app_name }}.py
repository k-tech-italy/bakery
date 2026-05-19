# Placeholder tests to satisfy the coverage gate on a fresh project.
# Replace these with real unit tests for your app logic.
import pytest

from {{ cookiecutter.package_name }}.{{ cookiecutter.first_app_name }}.exceptions import CoreError


def test_core_error_is_exception():
    assert issubclass(CoreError, Exception)


def test_core_error_can_be_raised():
    with pytest.raises(CoreError):
        raise CoreError("test error")


def test_core_error_message():
    error = CoreError("something went wrong")
    assert str(error) == "something went wrong"
