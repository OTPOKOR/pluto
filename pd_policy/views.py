from product.models import *
from django.views.generic import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect

class PolicyView(View):
    template_name = 'policy/index.html'
    categories = Item_Category.objects.all()
    
    def get(self,request,*args,**kwargs):
        if request.GET.get('category_id'):
            category_id = request.GET.get('category_id')
            selected_category = self.categories.get(id = category_id)
            req_spec_names = Ebay_Required_Spec_Name.objects.filter(foreign_category = category_id)
            return render(request, self.template_name,{'categories':self.categories,'selected_category':selected_category,'req_spec_names':req_spec_names})
        else:       
            return render(request, self.template_name,{'categories':self.categories})
    
    def post(self,request,*args,**kwargs):
        if request.POST.get('category_id'):
            category_id = request.POST.get('category_id')
            get_category_id = self.categories.get(id =category_id)
            category_name = request.POST.get('category_name')
            # categroy_name
            Item_Category.objects.filter(id = category_id).update(category_name=category_name)
            
            # req_spec_name
            req_spec_name_list = request.POST.getlist('req_spec_name','id')
            req_spec_names = Ebay_Required_Spec_Name.objects.filter(foreign_category = category_id)
            selected_spec_names = req_spec_names.values_list('id', flat=True)
            
            for i in range(len(req_spec_name_list)):
                try :
                    print(req_spec_name_list[i])
                    Ebay_Required_Spec_Name.objects.filter(id = selected_spec_names[i]).update(spec_name = req_spec_name_list[i])
                except IndexError:
                    print(req_spec_name_list[i])
                    Ebay_Required_Spec_Name.objects.create(foreign_category = get_category_id ,spec_name = req_spec_name_list[i])
                    pass
            # req_spec_name_end
            selected_category = self.categories.get(id = category_id)        
            return render(request,self.template_name,{'categories':self.categories,'selected_category':selected_category,'req_spec_names':req_spec_names})
        else:
            category_name = request.POST.get('category_name')
            return render(request,self.template_name,{'categories':self.categories})