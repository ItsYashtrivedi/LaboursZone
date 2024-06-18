from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'index.html')


def job(request):
    
    return render(request,'jobs.html')

def labourslist(request):
    return render(request,'labourslist.html')

def about(request):
    return render(request,'about.html')

def privacy(request):
    return render(request,'privacy.html')


