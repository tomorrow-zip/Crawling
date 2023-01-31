from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ChromeOptions

import chromedriver_autoinstaller
import time
import pandas as pd

import requests
from bs4 import BeautifulSoup as bs

class IkeaDriver(webdriver.Chrome):
    def set_url(self, url):
        self.get(url)
        self.implicitly_wait(30)

    def check_exists_by_xpath(self, xpath):
        try:
            self.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def click_by_xpath_until_end(self, xpath):
        while (self.check_exists_by_xpath(xpath)):
            try:
                self.find_element(By.XPATH, xpath).send_keys(Keys.ENTER)
                time.sleep(0.2)
            except ElementNotInteractableException:
                return

    




category_url = 'https://www.ikea.com/kr/ko/cat/chests-of-drawers-drawer-units-st004/'

opts = ChromeOptions()
opts.add_argument("--window-size=2560,1440")
chromedriver_autoinstaller.install()
driver = IkeaDriver(options=opts)

# 카테고리 링크로 들어가기
driver.set_url(category_url)

tmp = []

# 1) 소재 선택
# 1-1) 소재 탭 클릭
driver.find_element(By.XPATH, "//button[@aria-label='필터 모달 표시 소재']").send_keys(Keys.ENTER)
# 1-2) 소재 길이
MATERIAL_LEN = len(driver.find_element(By.ID, 'filter-MATERIAL').find_elements(By.CLASS_NAME, 'plp-checkbox__wrapper'))
for m in range(MATERIAL_LEN):
    if category_url != driver.current_url:
        driver.set_url(category_url)
        driver.find_element(By.XPATH, "//button[@aria-label='필터 모달 표시 소재']").send_keys(Keys.ENTER)
    # 1-3) 소재 선택 : 예외 처리?
    material = driver.find_element(By.ID, 'filter-MATERIAL').find_elements(By.CLASS_NAME, 'plp-checkbox__wrapper')[m]
    material_name = material.text
    material.send_keys(Keys.ENTER)
    material.send_keys(Keys.SPACE)
    time.sleep(2)

    category_material_url = driver.current_url

    # 2) 색상 선택
    # 2-1) 색상 탭 클릭
    driver.find_element(By.XPATH, "//button[@aria-label='필터 모달 표시 색상']").click()
    time.sleep(2)
    # 2-2) 색상 길이
    COLOR_LEN = len(driver.find_element(By.CLASS_NAME, 'plp-color-filter').find_elements(By.CLASS_NAME, 'plp-color-filter__input'))
    for c in range(COLOR_LEN):
        # 2-3) 색상 선택
        try:
            if category_material_url != driver.current_url:
                driver.set_url(category_material_url)
                driver.find_element(By.XPATH, "//button[@aria-label='필터 모달 표시 색상']").click()

            color = driver.find_element(By.CLASS_NAME, 'plp-color-filter').find_elements(By.CLASS_NAME, 'plp-color-filter__input')[c]
            color_name = color.text
            color.send_keys(Keys.ENTER)
            color.send_keys(Keys.SPACE)
            time.sleep(2)
        except ElementNotInteractableException:
            continue

        # 더보기 -> 전체 리스트 보기
        driver.click_by_xpath_until_end("//a[@aria-label='더 보기']")
        driver.find_element(By.XPATH, "//button[@aria-label='필터 모달 표시 색상']").click()
        time.sleep(1)

        # 상품 리스트 뽑아오기
        product_list = driver.find_elements(By.CLASS_NAME, 'plp-fragment-wrapper')
        
        for product in product_list:
            # 제품명 <span class="pip-header-section__title--small notranslate" translate="no">GRIMSBU 그림스부 </span>
            name = product.find_element(By.CLASS_NAME, 'pip-header-section__title--small').text
            
            # 가격 <span class="pip-price__integer">50,000</span>
            price = product.find_element(By.CLASS_NAME, 'pip-price__integer').text

            # 상품 링크 <a href="https://www.ikea.com/kr/ko/p/grimsbu-bed-frame-grey-20458757/" class="pip-product-compact__wrapper-link">
            link = product.find_element(By.CLASS_NAME, 'pip-product-compact__wrapper-link').get_attribute('href')

            # 상품 링크 바디 가져오기 이미지 / 사이즈 / 상품설명 가져오기
            link_body = bs(requests.get(link).content, 'html.parser')

            # 상품 설명 pip-product-summary__description
            if len(link_body.select('.pip-product-summary__description')) > 0:
                information = link_body.select('.pip-product-summary__description')[0].text

            # 사이즈 --> {어떤 형태로 ??. 왜 있는겨 이거}
            measure = link_body.select('.pip-product-dimensions__measurement-wrapper')
            measures = list(map(lambda x: x.text, measure))
            measure = ' '.join(measures)
            measure = measure.replace("\xa0", "")
            measure = measure.replace("\n", "")

            tmp.append([material_name, color_name, name, price, link, information, measure])

pd.DataFrame(tmp).to_csv('./chests.csv', index=False, header=False)
