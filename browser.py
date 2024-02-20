from typing import List, Any, Tuple

import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from loguru import logger
from selenium.webdriver.chrome.webdriver import WebDriver


class Undectable:

    def __init__(self, address, port_from_settings_browser, chrome_driver_path, headless):
        self.ser = Service(chrome_driver_path)
        self.chrome_options = Options()
        self.address = address
        self.port_from_settings_browser = port_from_settings_browser
        self.headless = headless
        # Send a request to the local API to get a list of profiles
        self.list_response = requests.get(f'http://{address}:{port_from_settings_browser}/list').json()['data']

    def get_proxy_by_name(self, name):
        return requests.get(
            f'http://{self.address}:{self.port_from_settings_browser}'
            f'/profile/getinfo/{self.get_id_by_name(name)}').json()['data']['proxy']

    def get_link_rotate_by_name(self, name):
        """Получить ссылку на ротацию прокси по имени"""
        proxy = self.get_proxy_by_name(name)
        return proxy[proxy.find(':http') + 1:]

    def get_proxy_by_id(self, id):
        return requests.get(
            f'http://{self.address}:{self.port_from_settings_browser}'
            f'/profile/getinfo/{id}').json()['data']['proxy']

    def get_link_rotate_by_id(self, id):
        """Получить ссылку на ротацию прокси по id"""
        proxy = self.get_proxy_by_id(id)
        return proxy[proxy.find(':http') + 1:]

    def get_id_by_name(self, name):
        """Получить профиль id по имени"""
        return [k for k, v in self.list_response.items() if v['name'] == name][0]

    def get_names_by_tag(self, tag):
        """Получить список имен профилей по тегу"""
        return [v['name'] for k, v in self.list_response.items() if tag in v['tags']]

    def get_ids_by_tag(self, tag):
        """Получить список id профилей по тегу"""
        return [k for k, v in self.list_response.items() if tag in v['tags']]

    def _start_profile(self, profile_id):
        if self.headless:
            params = 'chrome_flags=--headless=new'
        else:
            params = None
        return requests.get(f'http://{self.address}:{self.port_from_settings_browser}/profile/start/{profile_id}',
                            timeout=60, params=params)

    def startProfile_get_debug_port(self, profile_id):
        debug_port = self._start_profile(profile_id).json()['data']['debug_port']
        return debug_port

    def start_driver(self, debug_port):
        self.chrome_options.debugger_address = f'{self.address}:{debug_port}'
        driver = webdriver.Chrome(service=self.ser, options=self.chrome_options)
        return driver

    def stop_profile(self, profile_id):
        requests.get(
            f'http://{self.address}:{self.port_from_settings_browser}/profile/stop/{profile_id}')  # Stop profile

    def get_info_profile(self, profile_id):
        return requests.get(
            f'http://{self.address}:{self.port_from_settings_browser}'
            f'/profile/getinfo/{profile_id}').json()['data']


def start_profiles(browser: Undectable, tag, max_count=None) -> tuple[list[WebDriver], list[Any]]:
    """
    "Эта функция запускает несколько профилей браузера с указанным тегом.
    Параметры
    ----------
    :param browser:
    :param tag:
    :param max_count:
    :param tag str:
        Тег, который нужно искать в профилях браузера.

    :return:
    -------
    drivers : list Список объектов WebDriver для запущенных профилей."
    """

    # proxy = browser.get_proxy(name_profile)
    logger.info(f'Запуск профилей: {max_count}')
    id_profiles = browser.get_ids_by_tag(tag=tag)
    drivers = []
    for id in id_profiles[:max_count]:
        debug_port = browser.startProfile_get_debug_port(id)
        driver = browser.start_driver(debug_port)
        time.sleep(1)
        drivers.append(driver)
    logger.info('Профили запущены успешно')
    return drivers, id_profiles
