from asyncio.windows_events import NULL
from xmlrpc.client import Boolean
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from django.utils import timezone

# db모델 검색기능 'Q'
from django.db.models import Q
def index(request):
    """
    목록출력
    """
    # form = ProductSearch()'form':form
    product_list = Product.objects.order_by('-regist_date')
    return render(request,'manage/index.html',{'product_list':product_list},)

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
            print(type(value[0]))
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
    return render(request,'manage/index.html',{'product_list':product_list})