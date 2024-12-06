from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import logging
import time
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class _target_is(object):
    def __init__(self, locator, value):
        self.locator = locator
        self.value = value

    def __call__(self, driver):
        tittle = driver.find_element(*self.locator)
        if self.value == tittle.text:
            return True
        else:
            return False


def setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://accounts.snapchat.com/accounts/v2/login")
    return driver


def teardown(driver):
    driver.quit()


def process(name, password, file):
    driver = setup()

    driver.implicitly_wait(5)

    wait = WebDriverWait(driver, timeout=5)

    logger.critical("Complete config selenium!")

    # Enter Username page
    try:
        wait.until(
            _target_is(
                (
                    By.XPATH,
                    "//*[@id='account-identifier-root']/div/div[3]/article/div[1]/div[2]/h1",
                ),
                "Log in to Snapchat",
            )
        )
    except Exception:
        return "Wrong login URL"

    logger.critical("Found username input")

    time.sleep(2)
    try:
        _username = driver.find_element(
            by=By.XPATH, value="//*[@id='accountIdentifier']"
        )
        _username.send_keys(name)
        time.sleep(2)
        submit_button = driver.find_element(
            by=By.XPATH, value="//*[@id='account_identifier_form']/div[3]/button"
        )
        submit_button.click()
    except Exception:
        return "Cannot send username or email"

    logger.critical("Send username/email")

    # Enter Password page
    try:
        wait.until(
            _target_is(
                (By.XPATH, "//*[@id='password-root']/div/div[3]/article/div/div[2]/h1"),
                "Enter Password",
            )
        )
    except Exception:
        return "Cannot find enter password"

    logger.critical("Found password input")

    time.sleep(2)
    try:
        _password = driver.find_element(by=By.ID, value="password")
        _password.send_keys(password)
        time.sleep(2)
        submit_button = driver.find_element(
            by=By.XPATH, value="//*[@id='password_form']/div[3]/button"
        )
        submit_button.click()
    except Exception:
        return "Cannot send password"

    logger.critical("Send password input")

    # After Login page
    try:
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@id='__next']/div[1]/main/div[2]/div/div[1]/div/nav/div[3]/div[1]/a",
                )
            )
        )
    except Exception:
        return "Wrong username or password"

    logger.critical("Found welcome page")

    time.sleep(2)
    try:
        post_to_snapchat_button = driver.find_element(
            by=By.XPATH,
            value="//*[@id='__next']/div[1]/main/div[2]/div/div[1]/div/nav/div[3]/div[1]/a",
        )
        post_to_snapchat_button.click()
    except Exception:
        return "Cannot find post button"

    logger.critical("Clicked create new post")

    # Sign in page
    try:
        wait.until(
            _target_is(
                (By.XPATH, "//*[@id='__next']/main/div[2]/div[2]/div[2]/h1"),
                "Post to Snapchat",
            )
        )
    except Exception:
        return "Cannot find post page"

    logger.critical("Found create post page")

    time.sleep(2)
    try:
        sign_in_button = driver.find_element(
            by=By.XPATH,
            value="//*[@id='__next']/main/div[2]/div[2]/div[2]/div/div[2]/div/div/button",
        )
        sign_in_button.click()
    except Exception:
        return "Cannot find sign in button"

    logger.critical("Clicked sign in")

    # New post page
    try:
        wait.until(
            _target_is(
                (By.XPATH, "//*[@id='__next']/main/div[2]/div[2]/div[2]/div[2]"),
                "New Post",
            )
        )
    except Exception:
        return "Cannot sign in"

    logger.critical("Start upload image")

    time.sleep(2)
    try:
        post_to_my_story = driver.find_element(
            by=By.XPATH,
            value="//*[@id='__next']/main/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/div/div/div[2]/div/button",
        )
        post_to_my_story.click()

        time.sleep(0.5)
        public_story = driver.find_element(
            by=By.XPATH,
            value="//*[@id='__next']/main/div[2]/div[2]/div[2]/div[5]/div[3]/div/div[2]/div/div/div/div/div[2]/button",
        )
        public_story.click()

        time.sleep(0.5)
        try:
            if (
                accept_button := driver.find_element(
                    by=By.XPATH,
                    value="/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]",
                )
            ) is not None:
                accept_button.click()
        except Exception:
            pass
    except Exception:
        return "Cannot tick post to story / public story"

    logger.critical("Clicked tick upload")

    # Start upload image
    time.sleep(2)
    try:
        _file_name = secure_filename(file.filename)
        _file = file.read()
        try:
            folder_upload = os.path.abspath(os.path.join("image_upload"))
            print(folder_upload)
            os.rmdir(folder_upload)
        except Exception:
            pass
        os.makedirs("image_upload", mode=0o777, exist_ok=False)
        image_data = BytesIO(_file)
        image = Image.open(image_data)
        upload_file = os.path.abspath(os.path.join(f"image_upload/{_file_name}"))
        image.save(upload_file)
        choose_media = driver.find_element(
            by=By.XPATH,
            value="//*[@id='__next']/main/div[2]/div[2]/div[1]/div/div/input",
        )
        choose_media.send_keys(upload_file)
    except Exception as e:
        logger.critical(e)
        return "Cannot load image"

    logger.critical("Uploaded image")

    try:
        os.remove(upload_file)
    except Exception:
        pass

    # Wait for final post button clickable
    time.sleep(2)
    try:
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@id='__next']/main/div[2]/div[2]/div[2]/div[6]/div/div[2]/div/div[2]/div/button",
                )
            )
        )
        final_post_btn = driver.find_element(
            by=By.XPATH,
            value="//*[@id='__next']/main/div[2]/div[2]/div[2]/div[6]/div/div[2]/div/div[2]/div/button",
        )
        final_post_btn.click()
    except Exception:
        return "Image format have to be .PNG / .JPG and Resolution minimum: 1080x1920"

    logger.critical("Click final post button!")

    # After click final post, wait to success
    time.sleep(2)
    try:
        wait.until(
            _target_is(
                (
                    By.XPATH,
                    "/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div/button[2]",
                ),
                "Close",
            )
        )
    except Exception:
        return "Upload failed"

    logger.critical("Done")

    teardown(driver)

    logger.critical("Teardown selenium")

    return 1
