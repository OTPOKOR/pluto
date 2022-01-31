from asyncio.windows_events import NULL
from xmlrpc.client import Boolean
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from django.utils import timezone

# 페이징 처리
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# db모델 검색기능 'Q'
from django.db.models import Q

def index(request):
    """
    목록출력
    """
    # form = ProductSearch()'form':form
    product_list = Product.objects.order_by('-regist_date')
    # 페이지
    page = request.GET.get('page', '1')
    paginator = Paginator(product_list, 20)
    page_obj = paginator.get_page(page)
    
    save_page = {
        'site_choice_list':{
            '사이트1':'내셔널지오그래픽',
            '사이트2':'코닥',
            '사이트2':'스토어팜',
            },
        'page':page,
        '재고':'전체',
        'search':'',
        '검색조건':'전체검색'
    }
    
    return render(request,'manage/index.html',{'product_list':page_obj,'save_page':save_page})

def searchFormView(request):
    # 
    search = request.GET.get('search','')
    stock = request.GET.get('재고')
    재고 = '' if stock == '전체' else(True if stock =='재고'else False)
    사이트 = request.GET.getlist('사이트','value')
    검색조건 = request.GET.get('검색조건')
    
    # 사이트 리스트 풀어서 q 넣어주기
    site_choice_list = {}
    for i in range(len(사이트)):
        site_choice_list[f'사이트{i+1}'] = 사이트[i] 
    def create_q_source(*args):
        source=Q()
        for value in args:
            source &= Q(site = value[0])
        return source

    # 경우의수를 추가해서 q를 덮어씌운다
    q=Q()
    if 검색조건:
        if 검색조건 == '전체검색':
            q &= Q(product_name__icontains = search)|Q(identy_number__icontains = search)|Q(product_number__icontains = search)
        if 검색조건 == '식별번호':
            q &= Q(identy_number__icontains = search)
        if 검색조건 == '상품번호':
            q &= Q(product_number__icontains = search)
        if 검색조건 == '제품이름':
            q &= Q(product_name__icontains = search)
    if 사이트:
        q &= create_q_source(사이트)
    if type(재고) == bool:
        q &= Q(stock=재고)
    if 검색조건:
        q &= Q()
        
    product_list = Product.objects.filter(q).order_by('-regist_date') # 등록날짜순
    
    # 페이지
    page = request.GET.get('page','1')
    paginator = Paginator(product_list, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)
    
    save_page={
        'site_choice_list':site_choice_list,
        'page':page,
        '재고':stock,
        'search':search,
        '검색조건':검색조건
    }

    return render(request,'manage/index.html',{'product_list':page_obj,'save_page':save_page})