from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from pd_crawling.crawling_site.national import national_update
# 페이징 처리
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# db모델 검색기능 'Q'
from django.db.models import Q

# 이베이 업로드
from .ebay_upload.upload import *
# 리프레쉬 테스트
from .ebay_upload.refresh import *
def index(request):
    """
    목록출력
    """
    product_list = Product.objects.order_by('-regist_date')
    # 페이지
    page = request.GET.get('page', '1')
    paginator = Paginator(product_list, 20)
    page_obj = paginator.get_page(page)
    
    save_page = {
        'site_choice_list':{
            '사이트1':'내셔널지오그래픽',
            '사이트2':'코닥',
            '사이트3':'스토어팜',
            },
        'page':page,
        '재고':'전체',
        'search':'',
        '검색조건':'전체검색'
    }
    return render(request,'update/index.html',{'product_list':page_obj,'save_page':save_page})

def searchFormView(request):
    # 
    search = request.GET.get('search','')
    stock = request.GET.get('재고')
    재고 = '' if stock == '전체' else(True if stock =='재고'else False)
    사이트 = request.GET.getlist('사이트','value')
    검색조건 = request.GET.get('검색조건')
    
    # 사이트 반복문
    site_choice_list = {}
    for i in range(len(사이트)):
        site_choice_list[f'사이트{i+1}'] = 사이트[i] 
        
    # 사이트 리스트 풀어서 q 넣어주기
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
    product_list = Product.objects.filter(q).order_by('-regist_date')

    # 페이지
    page = request.GET.get('page','1')
    paginator = Paginator(product_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    save_page={
        'site_choice_list':site_choice_list,
        'page':page,
        '재고':stock,
        'search':search,
        '검색조건':검색조건
    }
    return render(request,'update/index.html',{'product_list':page_obj,'save_page':save_page})

def postUpdate(request):
    if request.method == 'POST':
        selected = request.POST.getlist('pd_check[]')
        # 다중 검색 필터 
        q_objects = Q(id__in=[])
        for item in selected:
            q_objects.add(Q(id=item),Q.OR)
        
        product_list = Product.objects.filter(q_objects).order_by('-regist_date')
    return render(request,'update/index.html',{'product_list':product_list})

def update(request):
    if request.method == 'POST':
        test = request.POST.getlist('pd_check[]')
    if request.method == "GET":
        if request.GET.get('선택'):
            selected = request.GET.getlist('pd_check[]')
            for item in selected:
                id_find = Product.objects.filter(Q(id=item))
                url = id_find.values()[0]['product_url']
                if 'naturestore' in url:
                    national_update(id_find,url)
        elif request.GET.get('이베이'):
            getInventoryItems()
            # selected = request.GET.getlist('pd_check[]')
            # for i in selected:
            #     # 이미지가 저장되지않으면 계속생성해야함 DB에 저장하는게 좋을거같음
            #     a = UploadingEbay(i)
            #     image_upload_list = a.image_upload()
            #     a.createOrReplaceInventoryItem(image_upload_list)
            #     a.createOffer()
            #     a.createOrReplaceInventoryItemGroup(image_upload_list)
            #     a.publishOfferByInventoryItemGroup()
        else :
            print('전체상품업데이트')
    return render(request,'update/index.html')

def refresh(request):
    refresh_tokken()
    return render(request,'update/test.html')