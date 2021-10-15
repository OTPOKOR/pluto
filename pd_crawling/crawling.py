import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

# 내셔널지오그래픽 크롤링
def nationalSearch(url):
    if url == None:
        return()

    res_url = url
    res = requests.get(res_url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    # 크롤링해오기
    get_image=soup.select_one('#mainImage > img')['src']
    product_image = 'https://www.naturestore.co.kr/'+get_image
    product_number=soup.select_one('div > div > div.item_detail_list > dl:nth-child(4) > dd').string
    product_name = soup.select_one('div > div > div.item_detail_tit > h3').string
    price = soup.select_one('div > div > div.item_detail_list > dl.item_price > dd > strong > strong').string

    # 보내보기
    context = [{
        'product_image':product_image,
        'url':url,
        'product_number':product_number,
        'product_name':product_name,
        'price':price,
    }]
    return(context)

def nationalSearchAll(url):
    if url == None:
        return()

    res_url = url
    res = requests.get(res_url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    
    name_list = []
    price_list = []
    url_list = []
    img_list = []

    context =[]
    # 이름
    for product_name in soup.find_all('strong','item_name'):
        name_list.append(product_name.get_text())
        
    # 가격
    for price in soup.find_all('strong','item_price'):
        price_list.append(price.get_text().strip().replace('원',''))

    # url
    for url in soup.find_all('div','item_photo_box'):
        siteurl = url.find('a')['href'].replace('.','')
        site = 'https://www.naturestore.co.kr/'+siteurl
        url_list.append(site)

    # 이미지
    for image in soup.find_all('div','item_photo_box'):
        siteimg = image.find('img')['src']
        img = 'https://www.naturestore.co.kr/'+siteimg
        img_list.append(img)


    # 모으기
    for i in range(len(name_list)):
        context.append({
            'product_name':name_list[i],
            'price':price_list[i],
            'url':url_list[i],
            'product_image':img_list[i],
        })
    
    return (context)
    
# 내셔널지오그래픽 크롤링 끝