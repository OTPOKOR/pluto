from django.urls import path

from . import views

app_name = 'crawling'

urlpatterns = [
    path('',views.index, name='index'),
    path('search/',views.SearchFormView, name='search'),
    path('save/',views.SaveProduct, name='save' ),
]