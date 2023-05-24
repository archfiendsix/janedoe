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


class HomePage(BasePage):
    def __init__(self, driver, test_sites):
        super().__init__(driver)
        self.driver = driver
        self.actions = ActionChains(self.driver)
        self.test_sites = test_sites
        self.timeout = 10

    def login(self, email, password):


        self.visit_page(self.test_sites["dev"])

        self.logger(f'Executing Login: {email}')

        login_button_locator = (By.XPATH, '//button[text()="LOG IN"]')

        login_button = self.wait_element(login_button_locator, 8)
        login_button.click()

        self.check_url('auth/login', False)

        username_locator = (By.CSS_SELECTOR, '#profile_name')
        # email = self.env_contractor_email

        self.wait_and_execute(self.driver, username_locator, 8, lambda elem: elem.send_keys(email))



        password_locator = (By.CSS_SELECTOR, '#password')
        # password = self.env_contractor_password
        self.wait_and_execute(self.driver, password_locator, 8,
                              lambda elem: elem.send_keys(password))
        eye_icon_locator = (By.CSS_SELECTOR, 'img[alt="eye-icon"]')
        self.wait_and_execute(self.driver, eye_icon_locator, 8,
                              lambda elem: elem.click())
        self.wait_and_execute(self.driver, eye_icon_locator, 8,
                              lambda elem: elem.click())
        login_button_locator = (By.XPATH, '//button[@type="submit"]')
        # self.wait_and_execute(self.driver, login_button[1], 8, lambda elem: elem.click())
        login_buttons = self.driver.find_elements(By.XPATH, '//button[@type="submit"]')
        login_buttons[0].click()

    def clickForgotPassword(self):
        self.logger('Clicking Forgot Password Button')
        forgotPassword_locator = (By.XPATH, '//a[@href="/auth/forgot_password"]')
        forgotPassword_button = self.wait_element(forgotPassword_locator, 8)
        forgotPassword_button.click()

    def clickSignUpForFreeButton(self):
        self.logger('Clicking Sign Up Button')
        signUpForFreeButton_locator = (By.XPATH, '//a[@href = "/auth/register_user"]')
        signUpForFree_button = self.wait_element(signUpForFreeButton_locator, 8)
        signUpForFree_button.click()

    def check_error(self, error_text):
        error_text_locator = (By.XPATH, '//*[starts-with(@class, "Formik_error")]')
        screen_error_text = self.wait_element(error_text_locator, 8).text

        assert error_text == screen_error_text, self.logger(f'Error message {error_text} wrong')
