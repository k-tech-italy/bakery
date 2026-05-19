import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from test_utils.factories import UserFactory


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--no-functional",
        action="store_true",
        default=False,
        help="Skip functional (browser) tests",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "functional: mark test as a functional (browser) test")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not config.getoption("--no-functional"):
        return
    skip_functional = pytest.mark.skip(reason="--no-functional flag provided")
    for item in items:
        if "functional" in item.keywords:
            item.add_marker(skip_functional)


@pytest.fixture(autouse=True, scope="session")
def tmp_media_root(tmp_path_factory):
    """Redirect all file uploads during tests to a temporary directory.

    Session-scoped so the same temp dir is shared across all tests in the run.
    Direct assignment (not override_settings) ensures the live server thread
    in functional tests sees the same value.
    """
    from django.conf import settings
    from django.core.files.storage import default_storage
    from django.utils.functional import empty

    media = tmp_path_factory.mktemp("media")
    settings.MEDIA_ROOT = str(media)
    default_storage._wrapped = empty  # force re-init with updated MEDIA_ROOT
    return media


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_user(db):
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def regular_user(db):
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client: APIClient, regular_user):
    token, _ = Token.objects.get_or_create(user=regular_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.fixture
def admin_client(api_client: APIClient, admin_user):
    token, _ = Token.objects.get_or_create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client
