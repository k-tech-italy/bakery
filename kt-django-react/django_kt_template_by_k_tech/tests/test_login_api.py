from django.urls import reverse
from .conftest import BaseTestCase
from ._extras.utils_test.factories import UserFactory


class LoginAPITest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login_url = reverse('login')
        self.user_password = 'testpass123'
        self.user = UserFactory(password=self.user_password)

    def test_successful_login(self):
        """Test Django API endpoint with valid credentials"""
        data = {
            'username': self.user.username,
            'password': self.user_password
        }
        response = self.client.post(self.login_url, data, format='json')
        assert response.status_code == 200

    def test_failed_login(self):
        data = {
            'username': 'ciao',
            'password': 'pippo'
        }
        response = self.client.post(self.login_url, data, format='json')
        assert response.status_code == 400

