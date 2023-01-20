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
import pandas as pd

class Driver:
    def __init__(self, url):
        self.driver = self.set_chrome_driver_auto()
        self.driver.get(url)
        self.driver.implicitly_wait(3) # 1초 기다리기

    def set_chrome_driver_auto(self):
        chromedriver_autoinstaller.install()
        return webdriver.Chrome()

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def click_by_xpath_until_end(self, xpath):
        while (self.check_exists_by_xpath(xpath)) :   
            btn = self.driver.find_element(By.XPATH, xpath)
            btn.send_keys(Keys.ENTER)
            time.sleep(1)

    def get_by_class_all(self, class_name):
        elements = self.driver.find_elements(By.CLASS_NAME, class_name)
        return elements

    def get_by_class(self, class_name):
        element = self.driver.find_element(By.CLASS_NAME, class_name)
        return element



if __name__ == '__main__':
    # 드라이버
    driver = Driver('https://www.ikea.com/kr/ko/cat/single-beds-16285/')
    
    # 더보기 눌러서 전체 리스트 보기
    driver.click_by_xpath_until_end('/html/body/main/div/div/div[4]/div[1]/div/div[3]/a')
    time.sleep(1)

    # 상품 리스트 뽑아오기
    product_list = driver.get_by_class_all('plp-fragment-wrapper')
    # print(f'product len : {len(product_list)}')

    # 각 상품 탐색
    imgs = []
    names = []
    prices = []
    links = []
    sizes = []
    infos = []
    for product in product_list:
        # 이미지
        imgs.append(product.find_element(By.CLASS_NAME, 'pip-image') .get_attribute('src'))

        # 제품명 <span class="pip-header-section__title--small notranslate" translate="no">GRIMSBU 그림스부 </span>
        names.append(product.find_element(By.CLASS_NAME, 'pip-header-section__title--small').text)

        # 가격 <span class="pip-price__integer">50,000</span>
        prices.append(product.find_element(By.CLASS_NAME, 'pip-price__integer').text)

        # 상품 링크 <a href="https://www.ikea.com/kr/ko/p/grimsbu-bed-frame-grey-20458757/" class="pip-product-compact__wrapper-link">
        link = product.find_element(By.CLASS_NAME, 'pip-product-compact__wrapper-link').get_attribute('href')
        links.append(link)
        
        # 사이즈 <span class="pip-header-section__description-measurement" data-ga-action="measurements_header_click" data-ga-label="90x200 cm">90x200 cm</span>
        sizes.append(product.find_element(By.CLASS_NAME, 'pip-header-section__description-measurement').text)

        # 상품설명 <div class="pip-product-details__container">
        information = bs(requests.get(link).content, 'html.parser').select('.pip-product-details__paragraph')
        info = ""
        for info_ in information:
            info += info_.text
        infos.append(info)

    df = pd.DataFrame(list(zip(names, imgs, prices, links, sizes, infos)))
    
    df.to_csv('./flist_indexFalse.csv', index=False, header=False)

