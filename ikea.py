import pandas as pd
from Crawling import *
import re, math

class Ikea:
    categori_len = 13
    categori_idx = [1, 1, 2, 3, 4, 5, 5, 5, 5, 6, 7, 7, 8]
    categori_url = [
        'https://www.ikea.com/kr/ko/cat/sofas-armchairs-fu003/',
        'https://www.ikea.com/kr/ko/cat/armchairs-couches-fu006/',
        'https://www.ikea.com/kr/ko/cat/sideboards-buffets-console-tables-30454/',
        'https://www.ikea.com/kr/ko/cat/beds-bm003/',
        'https://www.ikea.com/kr/ko/cat/wardrobes-19053/',
        'https://www.ikea.com/kr/ko/cat/cabinets-cupboards-st003/',
        'https://www.ikea.com/kr/ko/cat/chests-of-drawers-drawer-units-st004/',
        'https://www.ikea.com/kr/ko/cat/bookcases-shelving-units-st002/',
        'https://www.ikea.com/kr/ko/cat/trolleys-fu005/',
        'https://www.ikea.com/kr/ko/cat/tables-desks-fu004/',
        'https://www.ikea.com/kr/ko/cat/chairs-fu002/',
        'https://www.ikea.com/kr/ko/cat/bar-furniture-16244/',
        'https://www.ikea.com/kr/ko/cat/room-dividers-46080/'
    ]

    def __init__(self, idx=[0]):
        pass

    def get_max_page_url(self, url):
        list_total_count = bs(requests.get(url).content, 'html.parser').select('.catalog-product-list__total-count')[0].text
        print(list_total_count, end='. ')
        list_total_count = re.findall("[0-9]+", list_total_count)
        print(list_total_count)
        total_product = int(list_total_count[0])
        count_product = int(list_total_count[1])
        if count_product == 24 :
            page_number = math.ceil((total_product)/24)
        else :
            page_number = math.ceil((total_product+36)/48)
        print(f'product len : {total_product} / ', end='')

        return url+'?page='+str(page_number)


    
    def by_selenium(self, categori=None):
        driver = Driver('https://www.google.com/')
        
        if categori==None:
            categori = self.categori_url

        for url in categori:
            print(f'\n--[ {url} ]--')
            driver.set_url(self.get_max_page_url(url))

            # 상품 리스트 생성
            product_list = driver.get_by_class_all('plp-fragment-wrapper')
            print(f'{len(product_list)}. (total / count)')

            
            product = product_list[0]
            names = ['pip-image', 'pip-header-section__title--small', 'pip-price__integer', 'pip-product-compact__wrapper-link']
            for name in names:
                if (driver.check_exists_by_class(name, product)):
                    # print(f'{name} is exists')
                    if name == 'pip-product-compact__wrapper-link':
                        link = product.find_element(By.CLASS_NAME, 'pip-product-compact__wrapper-link').get_attribute('href')
                        link_body = bs(requests.get(link).content, 'html.parser')
                        information = link_body.select('.pip-product-details__paragraph')
                        measure = link_body.select('.pip-product-dimensions__measurement-wrapper')
                        if len(information)==0:
                            print(f'information-length is {len(information)}')
                        if len(measure)==0:
                            print(f'measure-length is {len(measure)}')
                else:
                    print(f'{name} is not exists')

            


def return_product_info_by_selenium(product):
    # 이미지
    img = product.find_element(By.CLASS_NAME, 'pip-image').get_attribute('src')

    # 제품명 <span class="pip-header-section__title--small notranslate" translate="no">GRIMSBU 그림스부 </span>
    name = product.find_element(By.CLASS_NAME, 'pip-header-section__title--small').text

    # 가격 <span class="pip-price__integer">50,000</span>
    price = product.find_element(By.CLASS_NAME, 'pip-price__integer').text

    # 상품 링크 <a href="https://www.ikea.com/kr/ko/p/grimsbu-bed-frame-grey-20458757/" class="pip-product-compact__wrapper-link">
    link = product.find_element(By.CLASS_NAME, 'pip-product-compact__wrapper-link').get_attribute('href')
    
    # 사이즈 <span class="pip-header-section__description-measurement" data-ga-action="measurements_header_click" data-ga-label="90x200 cm">90x200 cm</span>
    # sizes.append(product.find_element(By.CLASS_NAME, 'pip-header-section__description-measurement').text)

    # 상품설명 <div class="pip-product-details__container">
    # information = bs(requests.get(link).content, 'html.parser').select('.pip-product-details__paragraph')
    # info = ""
    # for info_ in information:
    #     info += info_.text
    # infos.append(info)

    return img, name, price, link


    

if __name__ == '__main__':
    ik = Ikea()
    ik.by_selenium()