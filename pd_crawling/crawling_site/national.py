# selenium

from asyncio.windows_events import NULL
from typing import List
from numpy import identity
from selenium import webdriver
import time
# 로딩완료대기 api
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
# BeatifulSoup
from bs4 import BeautifulSoup as BS
import requests as req
# class(str) 변경불가능변수
import copy
#정규식 찾기
import re

# //////////////////////단독실행 가능하게 만들어줌
# django 환경불러오기 상황에따라 제거가능..?
import os
# config,product,pluto,test 이 4가지중 한개로 테스트중
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

# 모델불러옴
from product.models import *

# 현재시간
import datetime

#폴더생성
import os
# 경로지정
import urllib.request

def national_crawling(url):
    # 크롤링
    # 옵션추가
    options = webdriver.ChromeOptions() 
    options.add_argument('window-size=1000,1000')
    options.add_argument('no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
    # 크롬세팅
    chrome = webdriver.Chrome(r"C:\Users\wldnj\Desktop\pluto\test\chromedriver.exe", options=options)

    # 사이트 접속 및 대기
    if '.php' in url:
        input_php_url = url
    else:
        # 주소에 php에 .이 안붙어서 반복문으로 직접붙임
        find_php = url.find('php')
        input_php_url = url[:find_php] +'.'+ url[find_php:]
    find_goodsNo = url.split('goodsNo=')
    goodsNo = find_goodsNo[1]
    # 사이트접속
    chrome.get(input_php_url)
    # 1초간 대기
    time.sleep(1)
    # BeatifulSoup로 페이지보냄
    res = chrome.page_source
    soup = BS(res,'html.parser')

    # 상품정보 추출
    상품이름 = soup.select_one('#frmView > div > div > div.item_detail_tit > h3').text
    상품번호 = soup.select_one('#frmView > div > div > div.item_detail_list > dl:nth-child(3) > dd').text
    식별번호 = goodsNo
    사이트이름 = '내셔널지오그래픽'
    업데이트날짜 = datetime.datetime.now()
    등록날짜 = datetime.datetime.now()
    사이트주소 = input_php_url
    브랜드이름 = '내셔널지오그래픽'
    imgUrlSource = soup.select_one('#lyZoom > div > div.ly_cont > div > div > div.item_photo_slide > ul > div > div > li.slick-slide.slick-current.slick-active > a > img')['src']
    imgUrl = imgUrlSource.replace('t50_','')
    imgUrlList = []
    imgUrlList.append(imgUrl)
    for i in range(4):
        i+=2
        if soup.select_one(f'#lyZoom > div > div.ly_cont > div > div > div.item_photo_slide > ul > div > div > li:nth-child({i}) > a > img'):
            ('#lyZoom > div > div.ly_cont > div > div > div.item_photo_slide > ul > div > div > li.slick-slide.slick-current.slick-active > a > img')
            imgUrlSource = soup.select_one(f'#lyZoom > div > div.ly_cont > div > div > div.item_photo_slide > ul > div > div > li:nth-child({i}) > a > img')['src']
            imgUrl = imgUrlSource.replace('t50_','')
            imgUrlList.append(imgUrl)
        else:
            pass
    
    if soup.select_one('#frmView > div > div > div.btn_choice_box.btn_restock_box > button.btn_add_soldout'):
        재고 = False
    else :재고 = True
    price_text = soup.select_one('#frmView > div > div > div.item_detail_list > dl:nth-child(1) > dd > span').text
    정가 = int(price_text.replace(',',''))
    sale_price_text = soup.select_one('#frmView > div > div > div.item_detail_list > dl.item_price > dd > strong > strong').text
    할인가격 = int(sale_price_text.replace(',',''))
    옵션 = []
    options = soup.select('#frmView > div > div > div.item_detail_list > div.item_add_option_box > dl > dd > select > option')
    for option in options:
        option_replace = option.text.replace(" ","").strip() #<class 'str'>
        option_sub = re.sub(r"[옵션:가격=\n]","",option_replace)
        if option_sub == '':
            continue
        else:
            옵션.append(option_sub)

    product_info = {
        'product_name': 상품이름,
        'product_number': 상품번호,
        'identy_number': 식별번호,
        'site':사이트이름,
        'regist_date':등록날짜,
        'product_url':사이트주소,
        'brand':브랜드이름,
        'stock' : 재고,
        'price' : 정가,
        'sale_price' : 할인가격,
        'shipping_price' : NULL,
        'update_date' : 업데이트날짜,
        'option' : 옵션
    }
    chrome.quit()
    return product_info,imgUrlList
    
    

def national_save(urls):
    # 이미지_저장
    def image_save(context,imgUrlList):
        try:
            url_base = 'https://www.naturestore.co.kr'
        # 경로저장
            path = "D:/DB/IMG/"+context['product_number']
            os.mkdir(path)
        # 이미지 url 리스트 반복문으로 저장
            for i in range(len(imgUrlList)):
                linkImg = url_base + imgUrlList[i]
                urllib.request.urlretrieve(linkImg,path+f"/{i}.jpg")
        except FileExistsError:
            print('이미 존재하는 파일입니다')
            pass

    for url in urls:
        try:
            pd_data = national_crawling(url)
            if Product.objects.filter(product_number =pd_data[0]['product_number']):
                print(pd_data[0]['product_name'] + '는 이미 저장된 상품입니다.')
            else:
                m = Product(**pd_data[0])
                m.save()
                for i in pd_data[0]['option']:
                    if "품절" in i:
                        stock = 0
                    else :
                        stock = 1
                    ProductOption.objects.create(
                        foreign_product = m,
                        option = i,
                        stock = stock
                    )
                image_save(pd_data[0],pd_data[1])
        except TypeError:
            pass
        
def national_update(pk_id,url):
    # DB 수정
    pd_data = national_crawling(url)
    del(pd_data[0]['regist_date'])
    m = Product.objects.filter(id__in = pk_id)
    for i in pd_data[0]['option']:
        if "품절" in i:
            stock = 0
        else :
            stock = 1
        e = ProductOption.objects.filter(foreign_product__in = m, option = i)
        e.update(stock = stock)
    m.update(**pd_data[0])
    print(pd_data[0])