import json
import os
import unittest
import time

from setup.test_setup import setup_test_environment
from pages.home_page import HomePage
from pages.dashboard_page import DashboardPage


class MainBoardTest(unittest.TestCase):
    def setUp(self):
        # Update paths to be platform-independent
        download_dir = os.path.abspath(os.path.join(os.getcwd(), "downloads"))
        # config_dir = os.path.abspath(os.path.join(os.getcwd(), "config.json"))
        torrent_dir = os.path.abspath(os.path.join(os.getcwd(), "fixtures"))
        testsites_dir = os.path.abspath(os.path.join(
            os.getcwd(), "fixtures/test_sites.json"))

        # Set driver
        self.driver = setup_test_environment()

        # Load configuration data and test site data from JSON files
        # with open(config_dir, "r") as json_file:
        #     self.config_data = json.load(json_file)
        with open(testsites_dir, "r") as test_sites_json_file:
            self.test_sites_data = json.load(test_sites_json_file)

        # Initialize page objects
        self.home_page = HomePage(self.driver, self.test_sites_data)
        self.dashboard_page = DashboardPage(self.driver, self.test_sites_data)

        self.driver.maximize_window()

    def test_home_login_links(self):

        self.home_page.visit_page(self.test_sites_data["dev"], "/auth/login")
        self.home_page.clickSignUpForFreeButton()
        self.home_page.check_url('/auth/register_user', exact=False)
        self.home_page.visit_page(self.test_sites_data["dev"], "/auth/login")
        self.home_page.clickForgotPassword()
        self.home_page.check_url('/auth/forgot_password', exact=False)


    def test_home_login_success(self):
        self.driver.get(self.test_sites_data["dev"])
        self.home_page.login(email=os.getenv("CONTRACTOR_EMAIL"), password=os.getenv("CONTRACTOR_PASSWORD"))
        self.home_page.check_url(text="girl/dashboard", exact=False)
        self.dashboard_page.logout()
        self.dashboard_page.check_url(text="https://dev.calljanedoe.com/", exact=True)

    def test_home_login_invalid_entries(self):
        self.home_page.visit_page(self.test_sites_data["dev"])

        self.home_page.login(email="", password=os.getenv("CONTRACTOR_PASSWORD"))
        self.home_page.check_error(error_text="Email is required")

        self.home_page.login(email="invalid@", password=os.getenv("CONTRACTOR_PASSWORD"))
        self.home_page.check_error(error_text="Email format is not valid")

        self.home_page.login(email=os.getenv("CONTRACTOR_EMAIL"), password="")
        self.home_page.check_error(error_text="Password is required")

        self.home_page.login(email=os.getenv("CONTRACTOR_EMAIL"), password="wrongpassword123")
        self.home_page.check_error(error_text="Email or password incorrect")

        self.home_page.login(email="unregistered@yahoo.com", password="wrongpassword123")
        self.home_page.check_error(error_text="User wasn't found")

    def tearDown(self):
        # Close the browser
        self.driver.quit()
