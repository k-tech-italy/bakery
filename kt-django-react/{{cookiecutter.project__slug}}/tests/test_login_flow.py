from .conftest import BaseWebApp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class LoginFrontendTest(BaseWebApp):

    localhost = 'http://localhost:5173/'

    def test_login_error(self):
        """Test React error message display"""
        self.driver.get(f'{self.base_url}/login')

        # Submit with wrong credentials
        username_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]')
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        username_input.send_keys(os.getenv('{{ cookiecutter.environ__prefix }}_ADMIN_USERNAME'))
        password_input.send_keys('wrongpass')

        submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
        submit_button.click()

        # Wait for and check error message
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'error-message'))
        )
        self.assertTrue(error_message.is_displayed())

    def test_login_success(self):
        """Test React  App Form login success"""
        self.driver.get(self.localhost + 'login')

        # Submit with right credentials
        username_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]')
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        username_input.send_keys(os.getenv('{{ cookiecutter.environ__prefix }}_ADMIN_USERNAME'))
        password_input.send_keys(os.getenv('{{ cookiecutter.environ__prefix }}_ADMIN_PASSWORD'))

        submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
        submit_button.click()
        # Wait the redirect to Home
        res = WebDriverWait(self.driver, 10).until(
            EC.url_to_be(self.localhost))

        home = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="home"]')
        self.assertTrue(home.is_displayed())

