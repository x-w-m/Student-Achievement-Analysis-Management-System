from datetime import datetime
from django.shortcuts import render


# Create your views here.
# main_views.py

def hello(request):
    return render(request, "hello.html")

