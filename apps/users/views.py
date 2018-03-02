from django.shortcuts import render, redirect
from models import *
from .. employers.models import *
from django.contrib import messages

def index(request):
    if 'user_id' in request.session or 'employer_id' in request.session or 'admin_id' in request.session:
        request.session.flush()
    return render(request, 'users/landing.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def resume(request, id):
    if 'user_id' in request.session:
        try:
            resume = Resume.objects.get(user_id = id)
            context = {
                "user" : User.objects.get(id=id),
                "resumes" : Resume.objects.filter(user_id = id),
                "workexperience" : WorkExperience.objects.filter(resume_id = resume.id),
                "education" : Education.objects.filter(resume_id = resume.id),
                "skills" : Skill.objects.filter(resume_id = resume.id),
            }
        except:
            context = {
                "user" : User.objects.get(id=id)
            }
        return render(request, 'users/resume.html', context)
    else:
        return redirect('/')

def process(request, action):
    if request.method == "POST":
        if action == "register":
            reg_user = User.objects.registration_validator(request.POST)
            if reg_user['status'] == "bad":
                for error in reg_user['data']:
                    messages.error(request, error)
                    return redirect('/signup')
            else:
                request.session['user_id'] = reg_user['data'].id
                return redirect('/jobs')

        elif action == "login":
            log_user = User.objects.login_validator(request.POST)
            if log_user['status'] == "bad":
                messages.error(request, log_user['data'])
                return redirect('/login')
            else:
                request.session['user_id'] = log_user['data'].id
                return redirect('/jobs')
        else:
            return redirect('/')
    else:
        return redirect('/')

def add(request, action):
    if 'user_id' in request.session:
        if request.method == "POST":
            if action == "address":
                user_address = Address.objects.address_validator(request.POST)
                if user_address['status'] == "bad":
                    for error in user_address['data']:
                        messages.error(request, error)
                        return redirect('/user/' + str(request.session['user_id']))
                else:
                    return redirect('/user/' + str(request.session['user_id']))
            elif action == "resume":
                user_resume = Resume.objects.resume_validator(request.POST)
                if user_resume['status'] == "bad":
                    for error in user_resume['data']:
                        messages.error(request, error)
                        return redirect('/user/' + str(request.session['user_id']) + "/resume")
                else:
                    return redirect('/user/' + str(request.session['user_id']) + "/resume")
            elif action == "experience":
                user_exp = Resume.objects.add_experience(request.POST)
                if user_exp['status'] == "bad":
                    for error in user_exp['data']:
                        messages.error(request, error)
                        return redirect('/user/' + str(request.session['user_id']) + '/new/work_experience')
                else:
                    return redirect('/user/' + str(request.session['user_id']) + '/resume')
            elif action == "education":
                user_edu = Resume.objects.add_education(request.POST)
                if user_edu['status'] == "bad":
                    messages.error(request, user_edu['data'])
                    return redirect('/user/' + str(request.session['user_id']) + '/new/education')
                else:
                    return redirect('/user/' + str(request.session['user_id']) + '/resume')
            else:
                return redirect('/user/' + str(request.session['user_id']))
        else:
            return redirect('/')
    else:
        return redirect('/')

def new(request, id, action):
    if 'user_id' in request.session:
        context = {
            "user" : User.objects.get(id = id),
            "resume" : Resume.objects.get(user_id = id)
        }
        if action == "work_experience":
            return render(request, 'users/new_experience.html', context)
        elif action == "education":
            return render(request, 'users/new_education.html', context)
        else:
            return redirect('/jobs')
    else:
        return redirect('/')
    

def edit_show(request, id, action):
    if 'user_id' in request.session:
        try:
            resume = Resume.objects.get(user_id = id)
            context = {
                "user" : User.objects.get(id=id),
                "resume" : Resume.objects.get(user_id = id),
                "address" : Address.objects.get(user_id = id),
                "skills" : Skill.objects.get(resume_id = resume.id)
            }
        except:
            context = {
                "user" : User.objects.get(id=id)
            }
        if action == "profile":
            return render(request, 'users/edit_profile.html', context)
        elif action == "resume":
            return render(request, 'users/edit_resume.html', context)
        else:
            return redirect('/user/' + str(request.session['user_id']))
    else:
        return redirect('/')
            
def edit(request, action):
    if 'user_id' in request.session:
        if request.method == "POST":
            if action == "profile":
                user_profile = User.objects.edit_profile(request.POST)
                if user_profile['status'] == "bad":
                    for error in user_profile['data']:
                        messages.error(request, error)
                    return redirect('/user/' + str(request.session['user_id']) + "/edit/profile")
                else:
                    return redirect('/user/' + str(request.session['user_id']))
            elif action == "address":
                user_address = Address.objects.edit_address(request.POST)
                if user_address['status'] == "bad":
                    for error in user_address['data']:
                        messages.error(request, error)
                    return redirect('/user/' + str(request.session['user_id']) + "/edit/profile")
                else:
                    return redirect('/user/' + str(request.session['user_id']))
            elif action == "resume":
                user_resume = Resume.objects.edit_resume(request.POST)
                if user_resume['status'] == "bad":
                    for error in user_resume['data']:
                        messages.error(request, user_resume['data'])
                    return redirect('/user/' + str(request.session['user_id']) + "/edit/resume")
                else:
                    return redirect('/user/' + str(request.session['user_id']) + "/resume")
            else:
                return redirect('/user/' + str(request.session['user_id']))
        else:
            return redirect('/user/' + str(request.session['user_id']))
    else:
        return redirect('/')

def users(request, ids):
    if 'user_id' in request.session:
        if request.session['user_id'] == int(ids):
            context = {
                "user" : User.objects.get(id=ids),
                "address" : Address.objects.filter(user_id = ids)
            }
            return render(request, 'users/self_show.html', context)
        else:
            return render(request, 'users/employer_show.html')
    else:
        return redirect('/')


def destroy(request, action, id):
    if 'user_id' in request.session:
        if action == "experience":
            WorkExperience.objects.get(id = id).delete()
            return redirect('/user/' + str(request.session['user_id']) + "/resume")
        elif action == "education":
            Education.objects.get(id = id).delete()
            return redirect('/user/' + str(request.session['user_id']) + "/resume")
        else:
            return redirect('/user/' + str(request.session['user_id']) + "/resume")
    else:
        return redirect('/')

def logout(request):
    if 'user_id' in request.session or 'employer_id' in request.session or 'admin_id' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')
                
