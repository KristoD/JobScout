from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    if not 'employer_id' in request.session:
        return redirect('/')
    else:
        context = {
            "employer" : Employer.objects.get(id = request.session['employer_id']),
        }
        return render(request, 'employers/dashboard.html', context)

def login(request):
    return render(request, 'employers/login.html')

def register(request):
    return render(request, 'employers/register.html')

def edit_company(request, id, action):
    if not 'employer_id' in request.session:
        return redirect('/')
    else:
        if action == "company":
            context = {
                "employer" : Employer.objects.get(id = request.session['employer_id']),
                "address" : EmployerAddress.objects.get(employer_id = request.session['employer_id'])
            }
        return render(request, 'employers/edit_company.html', context)

def listings(request, id):
    if not 'employer_id' in request.session:
        return redirect('/')
    else:
        context = {
            "employer" : Employer.objects.get(id = request.session['employer_id']),
            "address" : EmployerAddress.objects.get(employer_id = request.session['employer_id']),
            "listings" : Listing.objects.filter(employer_id = request.session['employer_id'])
        }
        return render(request, 'employers/listings.html', context)

def new_listing(request, id):
    if not 'employer_id' in request.session:
        return redirect('/')
    else:
        context = {
            "employer" : Employer.objects.get(id = request.session['employer_id']),
        }
        return render(request, 'employers/new_listing.html', context)    

def edit(request, action):
    if 'employer_id' in request.session:
        if request.method == "POST":
            if action == "company":
                edit_company = Employer.objects.edit_company(request.POST)
                if edit_company['status'] == "bad":
                    for error in edit_company['data']:
                        messages.error(request, error)
                    return redirect('/employers/company/' + str(request.session['employer_id']))
                else:
                    return redirect('/employers/company/' + str(request.session['employer_id']))
            elif action == "address":
                company_address = EmployerAddress.objects.edit_address(request.POST)
                if company_address['status'] == "bad":
                    for error in company_address['data']:
                        messages.error(request, error)
                    return redirect('/employers/company/' + str(request.session['employer_id']))
                else:
                    return redirect('/employers/company/' + str(request.session['employer_id']))

def company(request, id):
    if 'employer_id' in request.session:
        context = {
            "employer" : Employer.objects.get(id = request.session['employer_id']),
            "address" : EmployerAddress.objects.filter(employer_id = request.session['employer_id'])
        }
        return render(request, 'employers/company.html', context)
    else:
        return redirect('/')

def process(request, action):
    if request.method == "POST":
        if action == "register":
            reg_employer = Employer.objects.registration_validator(request.POST)
            if reg_employer['status'] == "bad":
                for error in reg_employer['data']:
                    messages.error(request, error)
                    return redirect('/employers/signup')
            else:
                if 'user_id' in request.session:
                    del request.session['user_id']
                request.session['employer_id'] = reg_employer['data'].id
                return redirect('/employers/dashboard')
        elif action == "login":
            log_employer = Employer.objects.login_validator(request.POST)
            if log_employer['status'] == "bad":
                messages.error(request, log_employer['data'])
                return redirect('/employers/signin')
            else:
                if 'user_id' in request.session:
                    del request.session['user_id']
                request.session['employer_id'] = log_employer['data'].id
                return redirect('/employers/dashboard')
        else:
            return redirect('/')
    else:
        return redirect('/')

def add(request, action):
    if 'employer_id' in request.session:
        if request.method == "POST":
            if action == "address":
                employer_address = EmployerAddress.objects.address_validator(request.POST)
                if employer_address['status'] == "bad":
                    for error in employer_address['data']:
                        messages.error(request, error)
                        return redirect('/employers/company/' + str(request.session['employer_id']))
                else:
                    return redirect('/employers/company/' + str(request.session['employer_id']))
            elif action == "listing":
                employer_listing = Listing.objects.listing_validator(request.POST)
                if employer_listing['status'] == "bad":
                    for error in employer_listing['data']:
                        messages.error(request, error)
                        return redirect('/employers/company/' + str(request.session['employer_id']) + "/new/listing")
                else:
                    return redirect('/employers/company/' + str(request.session['employer_id']) + "/listings")

def listing(request):
    return render(request, 'employers/listing.html')

def post(request):
    return redirect('/dashboard')
