from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    """
    목록출력
    """
    return render(request,'update/index.html')