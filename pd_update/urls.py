from django.urls import path

from . import views

app_name = 'update'

urlpatterns = [
    path('',views.index, name='index'),
    path('search/',views.searchFormView, name='search'),
    path('postUpdate/',views.postUpdate, name='postUpdate'),
    path('update/',views.update, name= 'update'),
    path('refresh/',views.refresh,name= 'refresh')
]