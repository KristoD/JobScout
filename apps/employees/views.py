from django.shortcuts import render, redirect
from .. users.models import *
from .. employers.models import *

def index(request):
    if 'user_id' in request.session:
        context = {
            "user" : User.objects.get(id = request.session['user_id']),
            "listings" : Listing.objects.all()
        }
        return render(request, 'employees/dashboard.html', context)
    else:
        return render(request, 'employees/dashboard.html')

def listing(request, id):
    if 'user_id' in request.session:
        context = {
            "listing" : Listing.objects.get(id=id),
            "user" : User.objects.get(id = request.session['user_id'])
        }
        return render(request, 'employees/listing.html', context)

def application_process(request, id):
    if 'user_id' in request.session:
        if request.method == "POST":
            listing = Listing.objects.get(id = id)
            listing.user_resumes.add(request.session['user_id'])
            listing.save()
            return redirect('/jobs')
        else:
            return redirect('/jobs')
    else:
        return redirect('/  ')
