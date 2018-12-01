from pathlib import Path
from time import sleep
import tldextract
import requests

from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome as Driver


class Webpage:
    """Render a webpage, given a browser instance.

    This class offers various ways of opening the webpage, and lets you
    take pictures at different sizes. """

    def __init__(self, url, driver: Driver):
        """
        :param driver: A selenium webdriver instance
        """
        self.driver = driver
        self.url = url

        # Load the page
        try:
            self.driver.get(url)

            try:
                self.driver.switch_to_alert().dismiss()
                print("Successfully dismissed alert!")
            except NoAlertPresentException:
                pass

            self.source = self.driver.page_source

            current_url = self.driver.current_url.replace("https://", "")
            current_url = current_url.replace("http://", "")
            current_url = current_url.replace("www.", "")
            current_url = current_url[:-1] if current_url[
                                                  -1] == "/" else current_url
            clean_url = url.replace("http://", "")
            clean_url = clean_url.replace("www.", "")
            assert current_url == clean_url, \
                f"URL should have been {clean_url}, was instead {current_url}"
        except Exception as e:
            raise e

    def save_screenshot(self, path: Path, dimensions, scroll_percent=0):
        """Render a screenshot at the given resolution
        :param path: A path to a .png file to save the image into
        :param dimensions: The (width, height) size of the window
        """

        assert Path(path).suffix == ".png", "The path must be a .png file!"

        # Scroll to a place in the window, by %

        try:
            max_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            self.driver.execute_script(
                f"window.scrollTo(0, {int(max_height * scroll_percent)});")
        except TimeoutError:
            print("Failed to take screenshot!")
            return

        self.driver.set_window_size(*dimensions)

        # Wait for browser to adjust
        sleep(.1)
        self.driver.save_screenshot(str(path))


def create_basic_driver(driver_path) -> Driver:
    # Open up browser window
    options = ChromeOptions()
    options.add_argument("--disable-notifications")
    driver = Driver(executable_path=str(driver_path),
                    options=options)
    driver.set_page_load_timeout(10)
    return driver
