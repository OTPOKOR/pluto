from django.urls import path

from . import views

app_name = 'update'

urlpatterns = [
    path('',views.index, name='index'),
    path('search/',views.searchFormView, name='search')
]