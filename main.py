from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ChromeOptions

import chromedriver_autoinstaller
import time, sys, re, math
import pandas as pd

import requests
from bs4 import BeautifulSoup as bs

category = {'sofas-armchairs-fu003' : 1,
    'armchairs-couches-fu006' : 1,
    'sideboards-buffets-console-tables-30454' : 2,
    'beds-bm003' : 3,
    'wardrobes-19053' : 4,
    'cabinets-cupboards-st003' : 5,
    'chests-of-drawers-drawer-units-st004' : 5,
    'bookcases-shelving-units-st002' : 5,
    'trolleys-fu005' : 5,
    'tables-desks-fu004' : 6,
    'chairs-fu002' : 7,
    'bar-furniture-16244' : 7,
    'room-dividers-46080' : 8}

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




def get_max_page_url(url):
    list_total_count = bs(requests.get(url).content, 'html.parser').select('.catalog-product-list__total-count')[0].text
    #print(list_total_count, end='. ')
    list_total_count = re.findall("[0-9]+", list_total_count)
    #print(list_total_count)
    total_product = int(list_total_count[0])
    count_product = int(list_total_count[1])
    if count_product == 24 :
        page_number = math.ceil((total_product)/24)
    else :
        page_number = math.ceil((total_product+36)/48)
    #print(f'product len : {total_product} / ', end='')

    return url+'?page='+str(page_number)

def product_list_to_csv(category_url = 'chests-of-drawers-drawer-units-st004'):
    category_idx = category[category_url]

    opts = ChromeOptions()
    opts.add_argument("--window-size=2560,1440")
    chromedriver_autoinstaller.install()
    driver = IkeaDriver(options=opts)

    # 카테고리 링크로 들어가기
    driver.set_url('https://www.ikea.com/kr/ko/cat/' + category_url)

    tmp = []

    # 더보기 -> 전체 리스트 보기
    driver.set_url(get_max_page_url('https://www.ikea.com/kr/ko/cat/' + category_url)) # 방법1 : 빠름
    # driver.click_by_xpath_until_end("//a[@aria-label='더 보기']") # 방법2
    time.sleep(1)

    # 상품 리스트 뽑아오기
    product_list = driver.find_elements(By.CLASS_NAME, 'plp-fragment-wrapper')
    time.sleep(1)
    print(f'product_len : {len(product_list)}\t', end='')
    product_list_percent = len(product_list)//10
    i = 0
    for product in product_list:
        time.sleep(0.1)
        if i%product_list_percent == 0:
            print('|', end='')

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

        tmp.append([category_idx, name, price, link, information, measure])
        i += i

    # to csv
    pd.DataFrame(tmp).to_csv(f'./data/{category_url}.csv', index=False, header=False)
    print()
    # `idx` int AUTO_INCREMENT NOT NULL ,
    # `type_idx` int  NOT NULL ,
    # `name` varchar(60)  NOT NULL ,
    # `price` int  NOT NULL ,
    # `site` varchar(100)  NOT NULL ,
    # `product_information` text  NULL ,
    # `size` varchar(255)  NULL ,
    # `status` varchar(10)  NOT NULL ,





if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'a':
            argv = range(len(category))
        else: argv = sys.argv[1:]
        for arg in argv:
            product_list_to_csv(list(category.keys())[int(arg)])
            time.sleep(1)
    else:
        product_list_to_csv()