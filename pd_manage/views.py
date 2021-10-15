from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from django.utils import timezone

def index(request):
    """
    목록출력
    """
    product_list = Product.objects.order_by('-regist_date')
    context = {'product_list':product_list}
    return render(request,'manage/index.html',context)