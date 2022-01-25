# selenium

from asyncio.windows_events import NULL
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
from product.models import Product

# 현재시간
import datetime

#폴더생성
import os
# 경로지정
import urllib.request
def national_save(urls):
    # 옵션추가
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1000,1000')
    options.add_argument('no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 크롬세팅
    chrome = webdriver.Chrome(r"C:\Users\wldnj\Desktop\pluto\test\chromedriver.exe", options=options)

    # 사이트 접속 및 대기
    wait = WebDriverWait(chrome,10)

    for url in urls:

        # 주소에 php에 .이 안붙어서 반복문으로 직접붙임
        find_php = url.find('php')
        input_php_url = url[:find_php] +'.'+ url[find_php:]
        find_goodsNo = url.split('goodsNo=')
        goodsNo = find_goodsNo[1]
        # 사이트접속
        chrome.get(input_php_url)
        # 2초간 대기
        time.sleep(2)
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

        # 이미지 경로
        imgUrl = soup.select_one('#contents > div > div:nth-child(8) > div.item_photo_info_sec > div > div > div.item_photo_slide > ul > div > div > li.slick-slide.slick-current.slick-active > a > img')['src']
        url_base = 'https://www.naturestore.co.kr'
        linkImg = url_base + imgUrl
        path = "D:/DB/IMG/"+상품번호

        
        # 
        # 재고
        if soup.select_one('#frmView > div > div > div.btn_choice_box.btn_restock_box > button.btn_add_soldout'):
            재고 = False
        else :재고 = True

        price_text = soup.select_one('#frmView > div > div > div.item_detail_list > dl.item_price > dd > strong > strong').text
        가격 = int(price_text.replace(',',''))
        옵션 = []
        options = soup.select('#frmView > div > div > div.item_detail_list > div.item_add_option_box > dl > dd > select > option')
        for option in options:
            test_option = option.text.replace(" ","").strip() #<class 'str'>
            test = re.sub(r"[옵션:가격=\n]","",test_option)
            if test == '':
                continue
            else:
                옵션.append(test)
                
        if Product.objects.filter(product_url=사이트주소):
            print(f'{상품이름}은 등록 되어있는 상품입니다')
        else:
            # 경로저장
            os.mkdir(path)
            # 이미지 저장
            urllib.request.urlretrieve(linkImg,path+"/01.jpg")
            print(f'상품이름 : {상품이름}\n상품번호 : {상품번호}\n식별번호 : {식별번호}\n 사이트이름 : {사이트이름} \n 등록날짜 : {등록날짜} \n 사이트주소 : {사이트주소}\n브랜드이름 : {브랜드이름} \n 재고 : {재고} \n 가격 : {가격}원 \n옵션 : {옵션}')
            Product.objects.create(product_name = 상품이름,product_number = 상품번호,identy_number = 식별번호,site = 사이트이름,regist_date =등록날짜,product_url = 사이트주소,brand = 브랜드이름,stock = 재고,price = 가격,shipping_price = NULL,update_date = 업데이트날짜,option = 옵션)
        
        # 사이트접속
        
    chrome.quit()