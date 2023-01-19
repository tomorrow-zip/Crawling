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

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def set_chrome_driver_auto():
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
    
    return webdriver.Chrome()

def check_exists_by_xpath(driver, xpath):
    try:
        t = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


if __name__ == '__main__':
    # 드라이버
    driver = set_chrome_driver_auto()
    
    driver.get('https://www.ikea.com/kr/ko/cat/single-beds-16285/')
    driver.implicitly_wait(3) # 3초 기다리기
    
    # 더보기 쫙
    while (check_exists_by_xpath(driver, '/html/body/main/div/div/div[4]/div[1]/div/div[3]/a')) :   
        nxt = driver.find_element(By.XPATH, '/html/body/main/div/div/div[4]/div[1]/div/div[3]/a')
        nxt.send_keys(Keys.ENTER)
        time.sleep(1)
    time.sleep(3)

    # 상품 리스트로 뽑아오기
    product_list = driver.find_elements(By.CLASS_NAME, 'plp-fragment-wrapper')
    print(f'product len : {len(product_list)}')

    # 각 상품 탐색
    imgs = []
    names = []
    prices = []
    links = []
    sizes = []
    infos = []
    for product in product_list:
        # 이미지
        image = product.find_element(By.CLASS_NAME, 'pip-image') 
        imgs.append(image.get_attribute('src'))

        # 제품명 <span class="pip-header-section__title--small notranslate" translate="no">GRIMSBU 그림스부 </span>
        name = product.find_element(By.CLASS_NAME, 'pip-header-section__title--small')
        names.append(name.text)

        # 가격 <span class="pip-price__integer">50,000</span>
        price = product.find_element(By.CLASS_NAME, 'pip-price__integer')
        prices.append(price.text)

        # 상품 링크 <a href="https://www.ikea.com/kr/ko/p/grimsbu-bed-frame-grey-20458757/" class="pip-product-compact__wrapper-link">
        link = product.find_element(By.CLASS_NAME, 'pip-product-compact__wrapper-link').get_attribute('href')
        links.append(link)
        
        # 사이즈 <span class="pip-header-section__description-measurement" data-ga-action="measurements_header_click" data-ga-label="90x200 cm">90x200 cm</span>
        size = product.find_element(By.CLASS_NAME, 'pip-header-section__description-measurement')
        sizes.append(size.text)

        # 상품설명 <div class="pip-product-details__container">
        information = bs(requests.get(link).content, 'html.parser').select('.pip-product-details__paragraph')
        info = ""
        for info_ in information:
            info += info_.text
        infos.append(info)

    df = pd.DataFrame(list(zip(names, imgs, prices, links, sizes, infos)))
    
    df.to_csv('./flist_indexFalse.csv', index=False, header=False)

