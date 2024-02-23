import random
import time
from loguru import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_recommendations(driver: WebDriver) -> None:
    """Clicks on the recommendations button in the driver."""
    try:
        driver.find_element(By.XPATH, '//a[@href="/app/recs"]').send_keys(Keys.ENTER)
    except Exception as ex:
        logger.error('Recommendations button not found')


# нажатие кнопки "Открыть профиль"
def click_open_profile(driver: WebDriver):
    try:
        wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
        buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div/div[@role="button"]')))
        buttons[1].send_keys(Keys.ENTER)
        logger.info('Кнопка "Открыть профиль" нажата')
    except Exception as ex:
        logger.error(f'Open profile button not found: {ex}')
        time.sleep(5)
        try:
            wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
            buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div/div[@role="button"]')))
            buttons[1].send_keys(Keys.ENTER)
            logger.info('Кнопка "Открыть профиль" нажата')
        except Exception as ex:
            logger.error('Open profile button not found {ex}')


def get_sliders(driver: WebDriver, name):
    try:
        sliders = driver.find_elements(
            By.XPATH, f'//div[@role="tablist" and contains(@aria-label,"{name}")]/button')
        return sliders
    except Exception as ex:
        logger.error('Slider not found')


# клик по кнопке Нет
def click_no(driver: WebDriver):
    # Xpath для кнопки NO не заходя в профиль
    #//button[@class="button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Bdrs(50%) P(0) Fw($semibold) focus-button-style Bxsh($bxsh-btn) Expand Trstf(e) Trsdu($normal) Wc($transform) Pe(a) Scale(1.1):h Scale(.9):a Bgi($g-ds-background-nope):a"]
    try:
        (driver.find_element(By.XPATH,
            '//button[@class="button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Bdrs(50%) P(0) Fw($semibold) focus-button-style Bxsh($bxsh-btn) Expand Trstf(e) Trsdu($normal) Wc($transform) Pe(a) Scale(1.1):h Scale(.9):a Bgc($c-ds-background-primary)"]')
         .send_keys(Keys.ENTER))
        logger.info('Кнопка "Нет" нажата')
    except Exception as ex:
        logger.error('No button not found')

