from django.shortcuts import render, redirect

def index(request):
    return render(request, 'employers/dashboard.html')

def register(request):
    return render(request, 'employers/register.html')

def info(request):
    return render(request, 'employers/info.html')

def listing(request):
    return render(request, 'employers/listing.html')

def post(request):
    return redirect('/dashboard')
