from django.shortcuts import render
from .. users.models import *

def index(request):
    if 'user_id' in request.session:
        context = {
            "user" : User.objects.get(id = request.session['user_id']),
        }
        return render(request, 'employees/dashboard.html', context)
    else:
        return render(request, 'employees/dashboard.html')