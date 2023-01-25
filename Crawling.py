from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import chromedriver_autoinstaller

import requests
from bs4 import BeautifulSoup as bs

import time

class Driver:
    def __init__(self, url):
        self.driver = self.set_chrome_driver_auto()
        self.driver.get(url)
        self.driver.implicitly_wait(20)

    def set_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(30)

    def set_chrome_driver_auto(self):
        chromedriver_autoinstaller.install()
        return webdriver.Chrome()

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_class(self, class_name, element=None):
        if element==None:
            element = self.driver
        try:
            element.find_element(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            return False
        return True

    def click_by_xpath_until_end(self, xpath):
        while (self.check_exists_by_xpath(xpath)) :   
            btn = self.driver.find_element(By.XPATH, xpath)
            btn.send_keys(Keys.ENTER)
            time.sleep(0.1)

    def get_by_class_all(self, class_name, element=None):
        if element==None:
            element = self.driver
        try:
            return self.driver.find_elements(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            return None

    def get_by_class(self, class_name, element=None):
        if element==None:
            element = self.driver
        element = element.find_element(By.CLASS_NAME, class_name)
        return element

    


