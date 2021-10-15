from django.shortcuts import render, get_object_or_404, redirect
from .forms import Searchform
from .crawling import *
def index(request):
    """
    목록출력
    """
    form = Searchform()
    return render(request,'crawling/index.html',{'form':form})

def SearchFormView(request):
    #사이트 복수선택용
    site_check = request.GET.get('search_url')
    # 사이트 선택
    site_select = request.GET.get('site_select')
    # 내셔널지오그래픽 선택시
    global getProductInfo

    if site_select == '내셔널지오그래픽':
        if site_check.find('goods_list') > 0:
            
            getProductInfo = nationalSearchAll(request.GET.get('search_url'))
        elif site_check.find('goods_view') > 0:
            
            getProductInfo = nationalSearch(request.GET.get('search_url'))
    # POST
    if request.method == 'POST':
        form= Searchform(request.POST)
        if form.is_valid():
            product_url = form.save(commit=False)
            return redirect('crawling/index.html')
    # GET
    else:
        form = Searchform()
    return render(request,'crawling/index.html',{'form':form,'getProductInfo':getProductInfo})


def SaveProduct(request):
    print('받아오는게없음')
    return render(request,'crawling/index.html',{'getProductInfo':getProductInfo})