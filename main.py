import time
from selenium.webdriver.common.keys import Keys

from browser import Undectable, start_profiles
from loguru import logger
from browser_managment import click_recommendations, click_open_profile, get_sliders, click_no
from data_processing import get_image_url, download_image, get_name, get_age, get_info_profile, Profile, \
    check_folder_name, check_folder, add_to_json
from selenium.webdriver.common.by import By

# Адрес сервера
ADDRESS = '127.0.0.1'
# Порт, указанный в настройках браузера
PORT_FROM_SETTINGS_BROWSER = '25325'
# Путь к драйверу Chrome
CHROME_DRIVER_PATH = 'C:\install\chromedriver121.exe'
# Имя профиля
NAME_PROFILE = '7476818'
# Имя тега
TAG_NAME = 'tinder'
# Количество профилей
COUNT_PROFILES = 1
# Настройка логирования
logger.add("logfile.log", rotation="500 MB", level="INFO")
# Путь к фотографиям
PATH_PHOTOS = 'photos'


def main():
    # URL сайта
    url = 'https://tinder.com/'
    # Создание экземпляра браузера
    browser = Undectable(ADDRESS, PORT_FROM_SETTINGS_BROWSER, CHROME_DRIVER_PATH, False)
    # Запуск профилей
    drivers, id_profiles = start_profiles(browser, TAG_NAME, COUNT_PROFILES)
    driver = drivers[0]

    # Если текущий URL не соответствует ожидаемому, переходим на ожидаемый URL
    if driver.current_url != 'https://tinder.com/app/recs':
        driver.get(url)
        time.sleep(5)
    # База данных профилей
    db = []
    while True:
        # Клик по рекомендациям
        click_recommendations(driver)

        driver.implicitly_wait(30)
        # Открытие профиля
        click_open_profile(driver)
        driver.implicitly_wait(30)
        time.sleep(3)

        # Получение имени, возраста и информации профиля
        name = get_name(driver)
        age = get_age(driver)
        info = get_info_profile(driver)

        # Получение слайдеров и URL изображений
        sliders = get_sliders(driver, name)
        urls_images = list()
        for i, slider in enumerate(sliders):
            slider.send_keys(Keys.ENTER)
            time.sleep(1)
            driver.implicitly_wait(30)
            urls_images.extend(get_image_url(driver))

        # Проверка имени папки и создание папки, если она не существует
        folders_name = check_folder_name(name, PATH_PHOTOS)
        if folders_name:
            list_num = [int(folder.split('_')[0]) for folder in folders_name]
            max_num = max(list_num)
            name_folder = f'{max_num + 1}_{name}'
            check_folder(name_folder, PATH_PHOTOS)

        else:
            name_folder = '1_' + name
            check_folder(name_folder, PATH_PHOTOS)

        # Скачивание изображений и сохранение их путей
        files_path = []
        for j, url in enumerate(set(urls_images)):
            file_path = f'{PATH_PHOTOS}/{name_folder}/{j}.jpg'
            files_path.append(file_path)
            download_image(url, file_path)

        time.sleep(1)
        # Создание профиля и добавление его в JSON
        profile = Profile(name, age, 'f', '\n '.join(info), files_path)

        add_to_json(profile)
        db.append(profile)

        # Клик по кнопке "Нет"
        click_no(driver)


if __name__ == '__main__':
    main()