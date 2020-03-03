# coding:utf-8
from django.shortcuts import render
import os

# Create your views here.

def index(request):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return render(request, os.path.join(PROJECT_ROOT, 'bookstore/templates/bookstore/index.html'))