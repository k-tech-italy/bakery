import os
import signal
import subprocess
import time
import typing
import urllib.error
import urllib.request

import pytest

if typing.TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")


@pytest.fixture(autouse=True, scope="session")
def serve_media_files_with_cors():
    """Add CORS headers to media responses served by the Django live server.

    Django's LiveServerThread wraps the WSGI app with _MediaFilesHandler, which
    bypasses django-cors-headers. We patch serve() to inject the CORS header so
    that the Vite preview server can fetch media files cross-origin.
    """
    from django.conf import settings
    from django.test.testcases import _MediaFilesHandler

    original_serve = _MediaFilesHandler.serve

    def _cors_serve(self, request):  # type: ignore[misc]
        response = original_serve(self, request)
        origin = request.META.get("HTTP_ORIGIN")
        if origin and origin in settings.CORS_ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
        return response

    _MediaFilesHandler.serve = _cors_serve  # type: ignore[method-assign]
    yield
    _MediaFilesHandler.serve = original_serve  # type: ignore[method-assign]


def _wait_for_server(url: str, timeout: int = 15) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2)  # noqa: S310
            return
        except (urllib.error.URLError, ConnectionError, OSError):
            time.sleep(0.5)
    raise TimeoutError(f"Server at {url} did not start within {timeout}s")


@pytest.fixture(scope="session")
def frontend_server(live_server):
    from django.conf import settings

    vite_preview_port = 5174
    frontend_url = f"http://localhost:{vite_preview_port}"

    if frontend_url not in settings.CORS_ALLOWED_ORIGINS:
        settings.CORS_ALLOWED_ORIGINS = [*settings.CORS_ALLOWED_ORIGINS, frontend_url]

    build_env = {k: v for k, v in os.environ.items() if not k.startswith("VITE_")}
    build_env["VITE_API_BASE"] = f"{live_server.url}/api"

    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, env=build_env, check=True, capture_output=True)

    preview_env = {k: v for k, v in os.environ.items() if not k.startswith("VITE_")}
    preview_proc = subprocess.Popen(
        ["npm", "run", "preview", "--", "--port", str(vite_preview_port), "--strictPort"],
        cwd=FRONTEND_DIR,
        env=preview_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    _wait_for_server(frontend_url)
    yield frontend_url

    preview_proc.send_signal(signal.SIGTERM)
    try:
        preview_proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        preview_proc.kill()


@pytest.fixture
def app_user(db) -> "AbstractUser":
    from test_utils.factories import UserFactory

    return UserFactory()
