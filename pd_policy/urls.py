from django.urls import path
from django.conf.urls import include
from . import views
from .views import *
app_name = 'policy'

urlpatterns = [
    path('',PolicyView.as_view(),name = 'index')
]