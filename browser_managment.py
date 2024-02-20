import random
import time
from loguru import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def click_recommendations(driver: WebDriver) -> None:
    """Clicks on the recommendations button in the driver."""
    try:
        driver.find_element(By.XPATH, '//a[@href="/app/recs"]').send_keys(Keys.ENTER)
    except Exception as ex:
        logger.error('Recommendations button not found')


# нажатие кнопки "Открыть профиль"
def click_open_profile(driver: WebDriver):
    try:
        driver.find_elements(By.XPATH, '//div/div[@role="button"]')[1].send_keys(Keys.ENTER)
    except Exception as ex:
        logger.error('Open profile button not found')


def click_slider(driver: WebDriver, name):
    try:
        slider = driver.find_elements(
            By.XPATH, f'//div[@role="tablist" and contains(@aria-label,"{name}")]/button')
        slider.click()
        time.sleep(1)
        slider.send_keys(Keys.ARROW_RIGHT)
    except Exception as ex:
        logger.error('Slider not found')

