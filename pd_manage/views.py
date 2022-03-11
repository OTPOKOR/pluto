from asyncio.windows_events import NULL
from xmlrpc.client import Boolean
from django.shortcuts import render, get_object_or_404, redirect
from numpy import product
from product.models import *
from django.utils import timezone

# 페이징 처리
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# db모델 검색기능 'Q'
from django.db.models import Q
# genericVeiw
from django.views.generic import *
# summernote
from .forms import FormFromSomeModel
# 경우에 따라서 가 아니라 통합해야할듯
class Index(View):
    template_name = 'manage/index.html'


    def get(self,request):

        product_list = Product.objects.order_by('-regist_date')

        # 페이지
        page = request.GET.get('page', '1')
        paginator = Paginator(product_list, 1)
        page_obj = paginator.get_page(page)

        # policy
        item_categories = Item_Category.objects.all()

        # 페이지 임시저장
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
        
        context ={
            "item_categories":item_categories,
            "product_list":page_obj,
            "save_page":save_page
        }        
        
        return render(request,self.template_name,context)

    def post(self,request):
        
        context = {
            
        }
        return render(request,self.template_name,context)
    
    
def index(request):

    product_list = Product.objects.order_by('-regist_date')
    # 페이지
    page = request.GET.get('page', '1')
    paginator = Paginator(product_list, 1)
    page_obj = paginator.get_page(page)
    # 아이템_카테고리
    item_categories = Item_Category.objects.all()
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
    
    return render(request,'manage/index.html',{'product_list':page_obj,'save_page':save_page,'item_categories':item_categories})

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
    paginator = Paginator(product_list, 1)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    save_page={
        'site_choice_list':site_choice_list,
        'page':page,
        '재고':stock,
        'search':search,
        '검색조건':검색조건
    }

    return render(request,'manage/index.html',{'product_list':page_obj,'save_page':save_page})

def titleUpdate(request):
    product_list = Product.objects.order_by('-regist_date')
        # 페이지
    page = request.GET.get('page','1')
    paginator = Paginator(product_list, 1)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    product_id = request.GET['product_id']
    product_title_value = request.GET['product_title']
    update_title = Product.objects.get(id=product_id)
    update_title.product_title = product_title_value
    update_title.save()
    return render(request,'manage/index.html',{'product_list':page_obj})


def policy(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        if Ebay.objects.filter(foreign_product = product_id):
            ebay_policy = Ebay.objects.get(foreign_product = product_id)
            des_find_id = Description_Middle.objects.filter(foreign_product = product_id).first()
            form = FormFromSomeModel(instance=des_find_id)
            return render(request,'manage/Policy/ebay_Policy.html',{'ebay_policy':ebay_policy,'product_id':product_id , 'form':form})
        else:
            return render(request,'manage/Policy/ebay_Policy.html',{'product_id':product_id})
    else :
        foreign_product = request.POST.get('product_id','')
        price = request.POST.get('price','')
        description = request.POST.get('description','')
        ddescription = request.POST.get('ddescription','')
        brand = request.POST.get('brand','')
        style = request.POST.get('style','')
        color = request.POST.get('color','')
        department = request.POST.get('department','')
        pattern = request.POST.get('pattern','')
        features = request.POST.get('features','')
        fabricType = request.POST.get('fabricType','')
        occasion = request.POST.get('occasion','')
        material = request.POST.get('material','')
        print(description)
        
        int_foreign_product = int(foreign_product)
        product_id = Product.objects.get( pk = int_foreign_product)

        if Description_Middle.objects.filter(foreign_product = foreign_product):
            e = Description_Middle.objects.filter(foreign_product = foreign_product)
            e.update(
                description = description
            )
        else: Description_Middle.objects.create(foreign_product = product_id , description = description)
        
        if Ebay.objects.filter(foreign_product = foreign_product):
            e = Ebay.objects.filter(foreign_product = foreign_product)
            e.update(
                price = price,
                brand = brand,
                style = style,
                color = color,
                department = department,
                pattern = pattern,
                features = features,
                fabricType = fabricType,
                occasion = occasion,
                material = material
            )
        else: 
            Ebay.objects.create(
                foreign_product = product_id,
                price = price,
                brand = brand,
                style = style,
                color = color,
                department = department,
                pattern = pattern,
                features = features,
                fabricType = fabricType,
                occasion = occasion,
                material = material
            )
        
        return render(request,'manage/Policy/ebay_Policy.html')
    
class TestView(ListView):
    
    model = Product
    paginate_by = 1
    template_name ="manage/test.html"
    context_object_name = 'product_list'

    def get_queryset(self):
        product_list = Product.objects.order_by('-regist_date')

        search = self.request.GET.get('search','')
        stock = self.request.GET.get('재고')
        재고 = '' if stock == '전체' else(True if stock =='재고'else False)
        사이트 = self.request.GET.getlist('사이트','value')
        검색조건 = self.request.GET.get('검색조건')
        if search :
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
            search_product_list = product_list.filter(q).order_by('-regist_date')
            return search_product_list
        return product_list
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        
        search = self.request.GET.get('search','')
        stock = self.request.GET.get('재고')
        사이트 = self.request.GET.getlist('사이트','value')
        검색조건 = self.request.GET.get('검색조건')
        
        print(사이트)
        print(type(사이트))
        context['search'] = search
        context['재고'] = stock
        context['사이트'] = 사이트
        context['검색조건'] = 검색조건

        paginator =context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)
        
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class PolicyForm(View):
    template_name = 'manage/Policy/ebay_Policy.html'

    def get(self,request):
        product_id = request.GET['product_id']
        # htmlParser
        des_find_id = Description_Middle.objects.filter(foreign_product = product_id).first()
        form = FormFromSomeModel(instance=des_find_id)
        # 전정책 테스트후 지우기
        ebay_policy = Ebay.objects.get(foreign_product = product_id)
        # spec_contain 접근해보자
        spec_names = Ebay_Required_Spec_Name.objects.filter(foreign_category = product_id).values_list('spec_name',flat=True)
        pd = Product.objects.get(id = product_id)
        spec_contains = Ebay_Required_Spec_Contain.objects.filter(foreign_product=pd)
        speclist = zip(spec_names,spec_contains)
        context={
            # 'spec_names':spec_names,
            # 'spec_contains':spec_contains,
            'speclist':speclist,
            'ebay_policy':ebay_policy,
            'product_id':product_id,
            'form':form
        }
    
        return render(request,self.template_name,context)


    def post(self,request):
        product_id = request.POST['product_id']
        test = Product.objects.get(id=product_id)
        # .values_list('id', flat=True)
        test1 = Ebay_Required_Spec_Name.objects.filter(foreign_category=product_id)
        for i in test1:
            print(i)
            Ebay_Required_Spec_Contain.objects.create(content_object=i,foreign_product = test,spec_contain = 'test')
        template_tag={
            
        }
    
        return render(request,self.template_name,template_tag)

    