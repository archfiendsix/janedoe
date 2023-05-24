import json
import logging
import os
import urllib3
# import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


webdriver_path = 'chromedriver.exe'


def setup_test_environment():
    # Load environment variables from .env file
    # load_dotenv()
    # Increase the maximum number of connections in the connection pool
    urllib3.PoolManager(maxsize=10)

    chrome_options = webdriver.ChromeOptions()
    # sessions_dir = os.path.abspath(os.path.join(os.getcwd(), "sessions"))

    # chrome_options.add_argument(f"--user-data-dir={sessions_dir}")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-beforeunload")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-session-crashed-bubble")

    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1,
        "credentials_enable_service": 1
    })

    driver = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

    # prefs = {"download.default_directory": download_dir}
    # chrome_options.add_experimental_option("prefs", prefs)

    # sessions_dir = os.path.abspath(os.path.join(os.path.expanduser("~"), ".chrome_sessions"))

    # sessions_dir = os.path.abspath(os.path.join(os.getcwd(), "sessions"))
    # # Create the folder if it doesn't already exist
    # os.makedirs(sessions_dir, exist_ok=True)
    # for session_file in os.listdir(sessions_dir):
    #     if session_file.endswith(".session"):
    #         with open(os.path.join(sessions_dir, session_file), "r") as f:
    #             cookie_data = f.read().strip().split("\n")
    #             cookies = {}
    #             for line in cookie_data:
    #                 name, value, domain, path, expires, secure, http_only = line.split("\t")
    #                 cookies[name] = {
    #                     "value": value,
    #                     "domain": domain,
    #                     "path": path,
    #                     "expires": expires,
    #                     "secure": secure,
    #                     "httpOnly": http_only
    #                 }
    #             for cookie in cookies.values():
    #                 driver.add_cookie(cookie)

    # Disable SSL warnings and set up logging
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s : %(message)s",
        handlers=[logging.StreamHandler()],
    )
    logging.getLogger().setLevel(logging.INFO)

    return driver
