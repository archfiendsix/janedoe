import logging
import pickle
import random
import time
import threading
import os
import pytesseract
import pygetwindow as gw
import pyautogui
import numpy as np
from PIL import ImageGrab
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

load_dotenv()


class BasePage:
    def __init__(self, driver):
        self.driver = driver,
        self.timeout = 10
        self.actions = ActionChains(self.driver)

        # Set environment variables
        self.env_contractor_email = os.getenv("CONTRACTOR_EMAIL")
        self.env_contractor_password = os.getenv("CONTRACTOR_PASSWORD")


    def dump_cookies(self):
        # with open("fixtures/cookies.pkl", "wb") as f:
        #     pickle.dump(self.driver.get_cookies(), f)
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open("fixtures/cookies.pkl", "wb"))

    def load_cookies(self):
        with open("fixtures/cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def try_interaction_thread(self):
        print("Interacting with page...\n")

        # define a function to do the scrolling
        def scroll_function(driver):
            scroll_direction = "down"
            while True:
                if scroll_direction == "down":
                    scroll_amount = random.randint(300, 1000)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                else:
                    scroll_amount = random.randint(500, 1000)
                    driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                time.sleep(random.randint(0, 1))  # wait for n seconds between scrolls
                if scroll_direction == "down" and driver.execute_script(
                        "return window.innerHeight + window.pageYOffset") >= driver.execute_script(
                    "return document.body.scrollHeight"):
                    scroll_direction = "up"
                elif scroll_direction == "up" and driver.execute_script("return window.pageYOffset") == 0:
                    scroll_direction = "down"

        # define a function to do the button click
        def click_function(driver):
            while True:
                try:
                    time.sleep(random.randint(0, 60))
                    soundcloud_skip_button_locator = (By.CSS_SELECTOR, ".skipControl__next")
                    self.wait_and_execute(driver, soundcloud_skip_button_locator, 10, lambda elem: elem.click())
                except (NoSuchElementException, TimeoutException):
                    pass

        # start the two threads
        scroll_thread = threading.Thread(target=scroll_function, args=(self.driver,))
        click_thread = threading.Thread(target=click_function, args=(self.driver,))
        scroll_thread.start()
        click_thread.start()

        # join the threads to wait for them to finish (optional)
        scroll_thread.join()

    def random_scroll(self, timeout):
        start_time = time.time()
        scroll_direction = 'down'
        while time.time() - start_time < timeout:

            if scroll_direction == "down":
                scroll_amount = random.randint(500, 1000)
                self.driver.execute_script(
                    f"window.scrollBy(0, {scroll_amount});")
            else:
                scroll_amount = random.randint(300, 800)
                self.driver.execute_script(
                    f"window.scrollBy(0, -{scroll_amount});")
            time.sleep(random.randint(1, 3))  # wait for n seconds between scrolls
            if scroll_direction == "down" and self.driver.execute_script(
                    "return window.innerHeight + window.pageYOffset") >= self.driver.execute_script(
                "return document.body.scrollHeight"):
                scroll_direction = "up"
            elif scroll_direction == "up" and self.driver.execute_script("return window.pageYOffset") == 0:
                scroll_direction = "down"

    def timeout_while_interact(self, timeout):
        print("Interacting with page...")
        start_time = time.time()
        scroll_direction = 'down'
        while time.time() - start_time < timeout:

            if scroll_direction == "down":
                scroll_amount = random.randint(500, 1000)
                self.driver.execute_script(
                    f"window.scrollBy(0, {scroll_amount});")
            else:
                scroll_amount = random.randint(500, 1000)
                self.driver.execute_script(
                    f"window.scrollBy(0, -{scroll_amount});")
            # time.sleep(random.randint(0, 1))  # wait for n seconds between scrolls
            if scroll_direction == "down" and self.driver.execute_script(
                    "return window.innerHeight + window.pageYOffset") >= self.driver.execute_script(
                "return document.body.scrollHeight"):
                scroll_direction = "up"
            elif scroll_direction == "up" and self.driver.execute_script("return window.pageYOffset") == 0:
                scroll_direction = "down"

            # Control for Soundcloud Music
            try:
                time.sleep(random.randint(1, 3))
                soundcloud_skip_button_locator = (By.CSS_SELECTOR, ".skipControl__next")
                self.wait_and_execute(self.driver, soundcloud_skip_button_locator, 10, lambda elem: elem.click())
            except (NoSuchElementException, TimeoutException):
                pass


    def wait_and_execute(self, driver, locator, timeout, action):
        time.sleep(random.randint(1, 2))

        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator))
        action(element)


    def wait_element(self, locator, timeout):
        time.sleep(random.randint(1, 2))

        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        return element

    @staticmethod
    def logger(text):
        logging.info(text)

    def get_active_window(self, window_title):
        partial_window_title = window_title
        all_windows = gw.getAllWindows()
        window = None
        for win in all_windows:
            if partial_window_title in win.title:
                window = win
                break

        if window is None:
            print(f"No window found with partial title '{partial_window_title}'")
            exit()

        return window

    def print_all_window_titles(self):
        all_windows = gw.getAllWindows()
        for win in all_windows:
            print(win.title)
    def open_window(self, window_title):
        # Set the path to the tesseract executable (Windows users)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # Ask the user for the partial title of the window to search within
        partial_window_title = window_title

        # Get all open windows
        all_windows = gw.getAllWindows()

        # Find the first window that contains the partial title
        window = None
        for win in all_windows:
            print(win.title)
            if partial_window_title in win.title:
                window = win
                break

        if window is None:
            print(f"No window found with partial title '{partial_window_title}'")
            exit()

        # Activate (bring to the front) the window
        window.activate()


    def application_action(self, window_title, element_text):

        time.sleep(15)

        # Update the window handle before grabbing the screenshot
        window = self.get_active_window(window_title)
        # Capture the window's content
        screenshot = ImageGrab.grab(
            bbox=(window.left, window.top, window.left + window.width, window.top + window.height))

        # Convert the image to grayscale
        gray_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

        # Set pytesseract configuration
        config = r'--psm 6 --oem 3'

        # Use pytesseract to extract text and their bounding boxes
        data = pytesseract.image_to_data(gray_screenshot, output_type=pytesseract.Output.DICT, config=config)

        search_text = element_text
        # Loop through the extracted data and check if any of the detected words match the search_text
        for i in range(len(data["text"])):
            if data["text"][i] == search_text:
                # Calculate the center coordinates of the bounding box
                x_center = data["left"][i] + data["width"][i] // 2
                y_center = data["top"][i] + data["height"][i] // 2

                # Calculate the screen coordinates by adding the window's position
                screen_x = window.left + x_center
                screen_y = window.top + y_center

                # Move the mouse to the center of the text and click
                pyautogui.moveTo(screen_x, screen_y)
                pyautogui.click()

                # Break the loop once the text has been found and clicked
                break
    def check_url(self, text,exact=False):
        # Wait for the page to load
        time.sleep(10)
        current_url = str(self.driver.current_url)
        if exact:
            assert text == current_url, self.logger(f'{text} redirection incorrect in {current_url}')
            self.logger(f'{text} redirection correct in {current_url}')
        else:
            assert text in current_url, self.logger(f'{text} redirection incorrect in {current_url}')
            self.logger(f'{text} redirection correct in {current_url}')

    def visit_page(self, base_url, sub=""):
        self.driver.get(base_url+sub)
        try:
            im_over_18_button_locator = (By.XPATH, '//button[text()="I AM OVER 18"]')
            im_over_18_button = self.wait_element(im_over_18_button_locator, 8)
            im_over_18_button.click()
            self.logger('I AM OVER 18 confirmed')
        except:
            pass
