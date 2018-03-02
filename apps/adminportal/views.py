from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
from .. users.models import *
from .. employers.models import *

def dashboard(request):
    if not 'admin_id' in request.session:
        return redirect('/admin')
    else:
        context = {
            "admin" : Admin.objects.get(id = request.session['admin_id']),
            "users" : User.objects.all(),
            "employers" : Employer.objects.all()
        }
        return render(request, 'adminportal/dashboard.html', context)

def user(request, id):
    if not 'admin_id' in request.session:
        return redirect('/')
    else:
        context = {
            "admin" : Admin.objects.get(id = request.session['admin_id']),
            "user" : User.objects.get(id=id)
        }
        return render(request, 'adminportal/user.html', context)

def employer(request, id):
    if not 'admin_id' in request.session:
        return redirect('/')
    else:
        context = {
            "admin" : Admin.objects.get(id = request.session['admin_id']),
            "employer" : Employer.objects.get(id=id)
        }
        return render(request, 'adminportal/employer.html', context)

def login(request):
    return render(request, 'adminportal/login.html')

def process(request, action):
    if request.method == "POST":
        if action == "login":
            admin_log = Admin.objects.login_validator(request.POST)
            if admin_log['status'] == "bad":
                messages.error(request, admin_log['data'])
                return redirect('/admin/login')
            else:
                request.session['admin_id'] = admin_log['data'].id
                print request.session['admin_id']
                return redirect('/admin/dashboard')
        else:
            return redirect('/admin')
    else:
        return redirect('/admin')

def ban(request, id, action):
    if request.method == "POST":
        if action == "user":
            user = User.objects.get(id = id)
            user.banned = True
            user.save()
            return redirect('/admin/user/' + str(user.id))
        elif action == "employer":
            employer = Employer.objects.get(id = id)
            employer.banned = True
            employer.save()
            return redirect('/admin/employer/' + str(employer.id))
        else:
            return redirect('/admin/dashboard')
    else:
        return redirect('/admin/dashboard')

def unban(request, id, action):
    if request.method == "POST":
        if action == "user":
            user = User.objects.get(id = id)
            user.banned = False
            user.save()
            return redirect('/admin/user/' + str(user.id))
        elif action == "employer":
            employer = Employer.objects.get(id = id)
            employer.banned = False
            employer.save()
            return redirect('/admin/employer/' + str(employer.id))
        else:
            return redirect('/admin/dashboard')
    else:
        return redirect('/admin/dashboard')