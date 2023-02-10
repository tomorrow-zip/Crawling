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

from main import IkeaDriver
from config import db

import pymysql

def download_image(url, file_path):
    with open(file_path, 'wb') as image:
        image.write(requests.get(url).content)



def image_to_file():
    opts = ChromeOptions()
    opts.add_argument("--window-size=2560,1440")
    chromedriver_autoinstaller.install()
    driver = IkeaDriver(options=opts)

    # MySQL Connection 연결
    conn = pymysql.connect(host=db['host'], user=db['user'], password=db['password'],
                       db=db['database'], charset='utf8')
    
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    
    # SQL문 실행
    sql = "SELECT idx, type_idx, site FROM furniture"
    curs.execute(sql)
    
    # 데이타 Fetch
    row = curs.fetchone()
    
    # (idx, categori_idx, product, price, link, info, size, status) -> idx, link
    while row:
        furniture_idx = row[0]
        categori_idx = row[1]
        link = row[2]

        # 링크 이동
        driver.get(link)
        driver.implicitly_wait(10)

        # 버튼 누르기
        # <button type="button" class="pip-btn pip-btn--small pip-btn--secondary pip-media-grid__button"><span class="pip-btn__inner"><span class="pip-btn__label">더 보기 </span></span></button>
        try:
            driver.find_element(By.CLASS_NAME, 'pip-media-grid__button').send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass

        # 이미지들 뽑아오기
        # pip-media-grid__grid 안에 있는 pip-image
        img = driver.find_element(By.CLASS_NAME, 'pip-media-grid__grid').find_elements(By.CLASS_NAME, 'pip-image')
        imgs = list(map(lambda x: x.get_attribute('src'), img))

        # 저장 idx, furniture_idx, files, files_cnt, status
        for cnt in range(len(imgs)):
            # tmp.append([furniture_idx, img]) 

            # {product_idx}-{cnt}.jpg
            download_image(imgs[cnt], f'./data/image/{furniture_idx}-{cnt}.jpg')

            if cnt == 0:
                download_image(imgs[cnt], f'./data/model_image/{categori_idx}/{furniture_idx}.jpg')
        
        row = curs.fetchone()

    #pd.DataFrame(tmp).to_csv(f'./data/image/{csv_path}.csv', index=False, header=False)

    # Connection 닫기
    conn.close()


def image_to_file_offset(offset, limit='501'):
    opts = ChromeOptions()
    opts.add_argument("--window-size=2560,1440")
    chromedriver_autoinstaller.install()
    driver = IkeaDriver(options=opts)

    # MySQL Connection 연결
    conn = pymysql.connect(host=db['host'], user=db['user'], password=db['password'],
                       db=db['database'], charset='utf8')
    
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    
    # SQL문 실행
    sql = "SELECT idx, type_idx, site FROM furniture LIMIT "+limit+" OFFSET "+offset # offset : 0, 500, 1000
    curs.execute(sql)
    
    # 데이타 Fetch
    row = curs.fetchone()
    
    # (idx, categori_idx, product, price, link, info, size, status) -> idx, link
    # ConnectionError
    while row:
        furniture_idx = row[0]
        categori_idx = row[1]
        link = row[2]

        if link == 'None':
            row = curs.fetchone()
            continue

        # 링크 이동
        driver.get(link)
        driver.implicitly_wait(3)

        # 버튼 누르기
        # <button type="button" class="pip-btn pip-btn--small pip-btn--secondary pip-media-grid__button"><span class="pip-btn__inner"><span class="pip-btn__label">더 보기 </span></span></button>
        try:
            driver.find_element(By.CLASS_NAME, 'pip-media-grid__button').send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass

        # 이미지들 뽑아오기
        # pip-media-grid__grid 안에 있는 pip-image
        img = driver.find_element(By.CLASS_NAME, 'pip-media-grid__grid').find_elements(By.CLASS_NAME, 'pip-image')
        imgs = list(map(lambda x: x.get_attribute('src'), img))

        # 저장 idx, furniture_idx, files, files_cnt, status
        for cnt in range(len(imgs)):
            # tmp.append([furniture_idx, img]) 

            # {product_idx}-{cnt}.jpg
            download_image(imgs[cnt], f'./data/image/{furniture_idx}-{cnt}.jpg')

            if cnt == 0:
                download_image(imgs[cnt], f'./data/model_image/{categori_idx}/{furniture_idx}.jpg')
                
        
        row = curs.fetchone()

    #pd.DataFrame(tmp).to_csv(f'./data/image/{csv_path}.csv', index=False, header=False)

    # Connection 닫기
    conn.close()

# 이케아 이미지
# ㄴ 카테고리 ID
# 	ㄴ 0001.jpg
# 	ㄴ 0002.jpg
# 	...


def image_to_file_offset_by_csv(start=0, end=10539):
    opts = ChromeOptions()
    opts.add_argument("--window-size=2560,1440")
    chromedriver_autoinstaller.install()
    driver = IkeaDriver(options=opts)

    # CSV 읽어오기
    tb = pd.read_csv('./furniture.csv', header=None)
    
    # (idx, categori_idx, product, price, link, info, size, status) -> idx, link
    # ConnectionError
    for i in range(start, end):
        furniture_idx = tb.iloc[i, 0]
        categori_idx = tb.iloc[i, 1]
        link = tb.iloc[i, 4]

        if link == 'None':
            continue

        # 링크 이동
        driver.get(link)
        driver.implicitly_wait(3)

        # 버튼 누르기
        # <button type="button" class="pip-btn pip-btn--small pip-btn--secondary pip-media-grid__button"><span class="pip-btn__inner"><span class="pip-btn__label">더 보기 </span></span></button>
        try:
            driver.find_element(By.CLASS_NAME, 'pip-media-grid__button').send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass

        # 이미지들 뽑아오기
        # pip-media-grid__grid 안에 있는 pip-image
        img = driver.find_element(By.CLASS_NAME, 'pip-media-grid__grid').find_elements(By.CLASS_NAME, 'pip-image')
        imgs = list(map(lambda x: x.get_attribute('src'), img))

        # 저장 idx, furniture_idx, files, files_cnt, status
        for cnt in range(len(imgs)):
            # tmp.append([furniture_idx, img]) 

            # {product_idx}-{cnt}.jpg
            download_image(imgs[cnt], f'./data/image/{furniture_idx}-{cnt}.jpg')

            if cnt == 0:
                download_image(imgs[cnt], f'./data/model_image/{categori_idx}/{furniture_idx}.jpg')
                

    #pd.DataFrame(tmp).to_csv(f'./data/image/{csv_path}.csv', index=False, header=False)




if __name__ == '__main__':
    if len(sys.argv) == 2:
        image_to_file_offset_by_csv(int(sys.argv[1])-3)
    elif len(sys.argv) == 3:
        image_to_file_offset_by_csv(int(sys.argv[1])-3, int(sys.argv[2])-3)
    else:
        image_to_file_offset_by_csv()
    
    # if len(sys.argv) == 2:
    #     image_to_file_offset(sys.argv[1]) # offset : 0, 500, 1000
    # elif len(sys.argv) == 3:
    #     image_to_file_offset(sys.argv[1], sys.argv[2]) # offset, limit(501)
    # else:
    #     image_to_file()

    
    



'''
LIMIT 501
OFFSET 500
'''