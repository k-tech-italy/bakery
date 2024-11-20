from pathlib import Path

from django.test import TestCase
from django.contrib.auth.models import User

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from selenium import webdriver


# class BaseServerTest:
#     def __init__(self, directory, port=0):
#         self.directory = directory
#         self.port = port
#         self.server = None
#         self.server_thread = None
#
#     def start(self):
#         handler = SimpleHTTPRequestHandler
#         handler.directory = self.directory
#         self.server = HTTPServer(('localhost', self.port), handler)
#
#         self.port = self.server.server_port
#
#         self.server_thread = threading.Thread(target=self.server.serve_forever)
#         self.server_thread.daemon = True
#         self.server_thread.start()
#         print(f"Starting server at: http://localhost:{self.server.server_port}")
#
#         return f"http://localhost:{self.port}"
#
#     def stop(self):
#         if self.server:
#             self.server.shutdown()
#             self.server.server_close()
#
#
# class BaseWebApp(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         if User.objects.count() == 0:
#             User.objects.create_superuser(username=os.getenv('{{ cookiecutter.environ__prefix }}_ADMIN_USERNAME'),
#                                           email=os.getenv('{{ cookiecutter.environ__prefix }}_ADMIN_EMAIL'),
#                                           password=os.getenv('{{ cookiecutter.environ__prefix }}_ADMIN_PASSWORD'))
#
#         static_build_dir = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src/{{cookiecutter.project__module}}/web/static/dist')).absolute()
#         print(static_build_dir)
#         cls.server = BaseServerTest(static_build_dir, port=5173)
#         cls.base_url = cls.server.start()
#         print(cls.base_url)
#
#         cls.driver = webdriver.Chrome()
#         cls.driver.implicitly_wait(10)
#
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         cls.server.stop()

