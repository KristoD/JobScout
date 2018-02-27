from __future__ import unicode_literals
from django.db import models
from ..users.models import *

class Employer(models.Model):
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_data = models.OneToOneField(User)

class Listing(models.Model):
    title = models.CharField(max_length=255)    
    decription = models.TextField()
    responsibilities = models.TextField()
    qualifications = models.TextField()
    required_experience = models.TextField()
    uploader = models.ForeignKey(Employer, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    