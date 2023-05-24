import os
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException, \
    ElementClickInterceptedException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, driver, test_sites):
        super().__init__(driver)
        self.driver = driver
        self.actions = ActionChains(self.driver)
        self.test_sites = test_sites
        self.timeout = 10
        self.logout_button_locator = (By.XPATH, '//a[@href = "/auth/logout"]')


    def logout(self):
        self.wait_and_execute(self.driver, self.logout_button_locator, 8, lambda elem: elem.click())
        self.logger('Logout successful')
