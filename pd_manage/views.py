from asyncio.windows_events import NULL
from xmlrpc.client import Boolean
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from django.utils import timezone

# 페이징 처리
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# db모델 검색기능 'Q'
from django.db.models import Q

# 페이징 함수
def paging(req,list):
    """페이징처리함수

    Args:
        req ([type]): 리퀘스트 받아온다
        list ([type]): 처리할 모델 리스트
    """
        # 입력파라미터
    page = req.GET.get('page', '1')  # 페이지
    # 페이징 처리
    paginator = Paginator(list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return page_obj

def index(request):
    """
    목록출력
    """
    # form = ProductSearch()'form':form
    product_list = Product.objects.order_by('-regist_date')
    page_obj = paging(request,product_list)
    return render(request,'manage/index.html',{'product_list':page_obj},)

def searchFormView(request):
    # 
    search = request.GET.get('search','')
    stock = request.GET.get('재고')
    재고 = '' if stock == '전체' else(True if stock =='재고'else False)
    사이트 = request.GET.getlist('사이트','value')
    
    # 사이트 리스트 풀어서 q 넣어주기
    def create_q_source(*args):
        source=Q()
        for value in args:
            source &= Q(site = value[0])
        return source

    # 경우의수를 추가해서 q를 덮어씌운다
    q=Q()
    if search:
        q &= Q(product_name__icontains = search)
    if 사이트:
        q &= create_q_source(사이트)
    if type(재고) == bool:
        q &= Q(stock=재고)

    # 등록날짜로 정렬
    product_list = Product.objects.filter(q).order_by('-regist_date')
    page_obj = paging(request,product_list)
    return render(request,'manage/index.html',{'product_list':page_obj})