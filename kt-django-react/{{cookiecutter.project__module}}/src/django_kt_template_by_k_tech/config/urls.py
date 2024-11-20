"""Django KT template by K-Tech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import posixpath
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls.conf import re_path

import mimetypes
import posixpath
from pathlib import Path

from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotModified
from django.utils._os import safe_join
from django.utils.http import http_date, parse_http_date
from django.utils.translation import gettext as _
from django.views.static import serve as static_serve

from {{ cookiecutter.project__module }}.web.views import LoginView

def serve(request, path, document_root=None, show_indexes=False):
    path = posixpath.normpath(path).lstrip("/")
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_file():
        return static_serve(request, path, document_root)
    else:
        return static_serve(request, "index.html", document_root)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin', admin.site.urls),
    path('auth/login/', LoginView.as_view(), name='login'),
    re_path(
        r"^(?P<path>.*)$",
        serve,
        {
            "document_root": env('FRONTEND_URL'),
        },
    ), # serve frontend files with path /fe/***
]

