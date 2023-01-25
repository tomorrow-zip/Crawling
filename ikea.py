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
        self.driver = Driver('https://www.google.com/')

    def get_product_list(self, url):
        self.driver.set_url(self.get_max_page_url(url))
        return self.driver.get_by_class_all('plp-fragment-wrapper')

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

    def get_product_data(self, product):
        link = self.get_link(product)
        return (self.get_image(product), self.get_title(product), self.get_price(product), link, self.get_info(link), self.get_size(link))

    def get_image(self, element):
        try:
            return self.driver.get_by_class('pip-image', element).get_attribute('src')
        except NoSuchElementException:
            return None

    def get_title(self, element):
        try:
            return self.driver.get_by_class('pip-header-section__title--small', element).text
        except NoSuchElementException:
            return None

    def get_price(self, element):
        try:
            return self.driver.get_by_class('pip-price__integer', element).text
        except NoSuchElementException:
            return None    

    def get_link(self, element):
        try:
            return self.driver.get_by_class('pip-product-compact__wrapper-link', element).get_attribute('href')
        except NoSuchElementException:
            return None

    def get_info(self, link):
        try:
            informations = bs(requests.get(link).content, 'html.parser').select('.pip-product-details__paragraph')
            return ' '.join(informations)
        except Exception:
            return None

    def get_size(self, link):
        try:
            informations = bs(requests.get(link).content, 'html.parser').select('.pip-product-dimensions__measurement-wrapper')
            return ' '.join(informations)
        except Exception:
            return None

    
    # categori : list
    def print_list(self, categori=None):
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
            print(self.get_product_data(product))
            

            


if __name__ == '__main__':
    ik = Ikea()
    ik.print_list(['https://www.ikea.com/kr/ko/cat/bar-furniture-16244/'])