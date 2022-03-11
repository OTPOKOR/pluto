from django.urls import path
from django.conf.urls import include
from . import views
from .views import TestView ,PolicyForm,Index
app_name = 'manage'

urlpatterns = [
    path('',views.index, name='index'),
    path('search/',views.searchFormView, name='search'),
    path('titleUpdate/',views.titleUpdate, name ='titleUpdate'),
    path('policy/',PolicyForm.as_view(),name='policy'),
    # 페이지 처리 떄문에 테스트로진행중
    path('test/',Index.as_view(), name='product_list'),
]   