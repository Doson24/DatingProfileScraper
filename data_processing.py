import random
import time
from loguru import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import requests
from dataclasses import dataclass, asdict
import json
# получение url изображения с сайта
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
import os


# dataclass для анкеты
@dataclass
class Profile:
    name: str
    age: str
    sex: str
    info: str
    media: list

    def to_dict(self):
        return asdict(self)


# Функция добавления записи в json файл Profile
def add_to_json(profile: Profile):
    data = []
    if not os.path.isfile('profiles.json'):
        with open('profiles.json', 'w') as file:
            json.dump(data, file)
    with open('profiles.json', 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    data.append(profile.to_dict())
    with open('profiles.json', 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(data, file, indent=2)


# def save_to_json(profiles: list[Profile]):
#     with open('profiles.json', 'w') as file:
#         json.dump([profile.to_dict() for profile in profiles], file, indent=2)


# Функция проверки на наличие папки с именем name, если нет, то создает ее
def check_folder(name: str, path: str = 'photos'):
    path = f'{path}/{name}'
    if not os.path.exists(path):
        os.makedirs(path)


# Функция проверяет все имена папок на наличие в имени части name
def check_folder_name(name: str, path: str) -> list[str]:
    return [folder for folder in os.listdir(f'{path}/') if name in folder]


def get_info_profile(driver: WebDriver) -> list:
    """Get the name of the person whose profile is open."""
    try:
        block_info = driver.find_elements(By.XPATH, '//div[contains(@class,"profileCard")]/div[2]/div')
        return [_.text for _ in block_info[:-2]]
    except Exception as ex:
        logger.error(f'Profile info not found: {ex}')


def get_image_url(driver: WebDriver) -> list:
    wait = WebDriverWait(driver, 30)  # wait for up to 10 seconds
    images = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@role="img" and contains(@class, "profileCard")]')))
    return [image.get_attribute('style').split('url("')[1].split('")')[0]
            for image in images]


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


def delete_duplicates(filename):
    """
    Функция для удаления дубликатов из файла 'profiles.json'.
    Если в файле 'profiles.json' есть профили с одинаковыми именами, функция удаляет все дубликаты, оставляя только один профиль.
    После удаления профиля, функция также удаляет все связанные с ним файлы изображений.
    """
    # Открываем файл 'profiles.json' для чтения
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        # Загружаем данные из файла
        data = json.load(file)
    # Создаем список имен всех профилей
    info = [profile['info'] for profile in data]
    # Проходим по всем уникальным именам
    for name in set(info):
        # Если имя встречается более одного раза
        if info.count(name) > 1:
            # Проходим по всем профилям
            for profile in data:
                info = [profile['info'] for profile in data]
                if info.count(name) == 1:
                    break
                # Если имя профиля совпадает с текущим именем
                if profile['info'] == name:
                    # Удаляем профиль из списка
                    data.remove(profile)
                    # Удаляем все файлы изображений, связанные с профилем
                    for file in profile['media']:
                        try:
                            os.remove(file)
                        except:
                            print('Нет файла:', file)
                    try:
                        os.removedirs(file.split('/')[0] + '/' + file.split('/')[1])
                    except:
                        print('Отсутствует папка:', file.split('/')[0] + '/' + file.split('/')[1])
    # Открываем файл 'profiles.json' для записи
    with open('no_duplicates_profiles.json', 'w', encoding='utf-8', errors='ignore') as file:
        # Записываем обновленные данные в файл
        json.dump(data, file, indent=2)


if __name__ == '__main__':
    delete_duplicates('profiles.json')
