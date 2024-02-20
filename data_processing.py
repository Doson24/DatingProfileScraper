import random
import time
from loguru import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import requests


# получение url изображения с сайта
def get_image_url(driver: WebDriver):
    # images = browser.find_elements(By.XPATH, '//span/div[@role="img"]')

    # images = browser.find_elements(By.XPATH, '//span[contains(@class, "keen")]')
    images = driver.find_elements(By.XPATH, '//*[@role="img" and contains(@class, "profileCard")]')
    for image in images:
        if image.get_attribute('style') != '':
            yield image.get_attribute('style').split('url("')[1].split('")')[0]



def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        logger.error(f'Image not found: {url}')

def get_name(browser: WebDriver) -> str:
    """Get the name of the person whose profile is open."""
    try:
        return browser.find_element(By.XPATH, '//h1').text
    except Exception as ex:
        logger.error(f'Name not found: {ex}')


def get_age(browser: WebDriver) -> str:
    """Get the age of the person whose profile is open."""
    try:
        return browser.find_element(By.XPATH, "//h1/../following-sibling::*").text
    except Exception as ex:
        logger.error(f'Age not found: {ex}')


if __name__ == '__main__':
    get_image_url()
