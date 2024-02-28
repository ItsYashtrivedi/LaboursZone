from django.shortcuts import render

# Create your views here.
def register_home(request):
    return render(request, 'register/register_home.html')
def register_labour(request):
    
    return render(request, 'register/register_labour.html')
def register_contractor(request):
    
    return render(request, 'register/register_contractor.html')