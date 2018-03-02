from __future__ import unicode_literals

from django.db import models
from .. employers.models import *
import bcrypt
import re
from datetime import date
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
today = date.today()

class UserManager(models.Manager):
    def registration_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append("First and last name should be more than 2 characters.")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors.append("First and last name can only contain alphabetic characters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be in correct format.")
        if len(postData['password']) < 8:
            errors.append("Password must be 8 or more characters!")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords must match!")
        if len(User.objects.filter(email = postData['email'])):
            errors.append("Email is already in use.")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed_pw)
            res['data'] = user
        return res

    def login_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        try:
            the_user = User.objects.get(email = postData['email'])
        except:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res
        if the_user.banned == True:
            res['status'] = "bad"
            res['data'] = "Sorry pal. You've been banned. If you feel this was a mistake, send us an email. You probably will never get a response."
            return res
        if bcrypt.checkpw(postData['password'].encode(), the_user.password.encode()):
            res['data'] = the_user
            return res
        else:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res

    def edit_company(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        user = User.objects.get(id = postData['user_id'])
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append("First and last name should be more than 2 characters.")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors.append("First and last name can only contain alphabetic characters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be in correct format.")
        if postData['email'] != user.email:
            if len(User.objects.filter(email = postData['email'])):
                errors.append("Email is already in use.")
        if postData['password'] != "":
            if len(postData['password']) < 8:
                errors.append("Password must be 8 or more characters!")
            if postData['password'] != postData['confirm_password']:
                errors.append("Passwords must match!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            if postData['password'] != "" and postData['email'] != user.email:
                hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
                user.first_name = postData['first_name']
                user.last_name = postData['last_name']
                user.email = postData['email']
                user.password = hashed_pw
                user.save()
            elif postData['email'] != user.email:
                user.first_name = postData['first_name']
                user.last_name = postData['last_name']
                user.email = postData['email']
                user.save()
            else:
                user.first_name = postData['first_name']
                user.last_name = postData['last_name']
                user.save()
            res['data'] = user
        return res


        

class AddressManager(models.Manager):
    def address_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['zip_code']) != 5:
            errors.append("Zip code must be 5 digits!")
        if len(postData['city']) < 2:
            errors.append("City must be 2 characters or longer!")
        if len(postData['phone']) != 10:
            errors.append("Invalid phone number!")
        if len(postData['state']) != 2:
            errors.append("State must be 2 characters in all capital letters.")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            address = Address.objects.create(address = postData['address'], city = postData['city'], state = postData['state'], zip_code = postData['zip_code'], phone = postData['phone'], user_id = postData['user_id'])
            res['data'] = address
        return res

    def edit_address(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['zip_code']) != 5:
            errors.append("Zip code must be 5 digits!")
        if len(postData['city']) < 2:
            errors.append("City must be 2 characters or longer!")
        if len(postData['phone']) != 10:
            errors.append("Invalid phone number!")
        if len(postData['state']) != 2:
            errors.append("State must be 2 characters in all capital letters.")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            address = Address.objects.get(user_id = postData['user_id'])
            address.address = postData['address']
            address.state = postData['state']
            address.city = postData['city']
            address.zip_code = postData['zip_code']
            address.phone = postData['phone']
            address.save()
            res['data'] = address
        return res

class ResumeManager(models.Manager):
    def resume_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['job_title']) < 1:
            errors.append("You must enter a job title!")
        if len(postData['company']) < 1:
            errors.append("You must enter a company name!")
        if len(postData['job_city']) < 1:
            errors.append("You must enter a city!")
        startExperience = datetime.strptime(postData['time_start'], "%Y-%m-%d")
        endExperience = datetime.strptime(postData['time_end'], "%Y-%m-%d")
        if endExperience.date() > date.today():
            errors.append("End date must be a valid date!")
        if len(postData['job_description']) < 1:
            errors.append("You must enter your job's description!")
        if len(postData['skills']) < 1:
            errors.append("Yo must enter your skills!")
        time1 = postData['edu_time_start']
        time2 = postData['edu_time_end']
        if time2 != "":
            startEducation = datetime.strptime(time1, "%Y-%m-%d")
            endEducation = datetime.strptime(time2, "%Y-%m-%d")
            if endEducation.date() > date.today():
                errors.append("End date must be a valid date!")
        else:
            time1 = None
            time2 = None
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            resume = Resume.objects.get_or_create(about_self = postData['about_self'], desired_job = postData['desired_job'], user_id = postData['user_id'])
            WorkExperience.objects.create(job_title = postData['job_title'], company = postData['company'], city = postData['job_city'], time_start = startExperience, time_end = endExperience, description = postData['job_description'], resume_id = resume[0].id)
            if postData['edu_time_end'] != "":
                Education.objects.create(degree = postData['degree'], school = postData['school'], study = postData['study'], city = postData['edu_city'], time_start = startEducation, time_end = endEducation, resume_id = resume[0].id)
            else:
                Education.objects.create(degree = postData['degree'], school = postData['school'], study = postData['study'], city = postData['edu_city'], time_start = time1, time_end = time2, resume_id = resume[0].id)
            Skill.objects.create(skills = postData['skills'], resume_id = resume[0].id)
            res['data'] = resume
        return res

    def add_experience(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['job_title']) < 1:
            errors.append("You must enter a job title!")
        if len(postData['company']) < 1:
            errors.append("You must enter a company name!")
        if len(postData['job_city']) < 1:
            errors.append("You must enter a city!")
        startExperience = datetime.strptime(postData['time_start'], "%Y-%m-%d")
        endExperience = datetime.strptime(postData['time_end'], "%Y-%m-%d")
        if endExperience.date() > date.today():
            errors.append("End date must be a valid date!")
        if len(postData['job_description']) < 1:
            errors.append("You must enter your job's description!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            work = WorkExperience.objects.create(job_title = postData['job_title'], company = postData['company'], city = postData['job_city'], time_start = startExperience, time_end = endExperience, description = postData['job_description'], resume_id = postData['resume_id'])
            res['data'] = work
        return res
    
    def add_education(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        time1 = postData['edu_time_start']
        time2 = postData['edu_time_end']
        if time2 != "":
            startEducation = datetime.strptime(time1, "%Y-%m-%d")
            endEducation = datetime.strptime(time2, "%Y-%m-%d")
            if endEducation.date() > date.today():
                res['status'] = "bad"
                res['data'] = "End date must be a valid date!"
            else:
                edu = Education.objects.create(degree = postData['degree'], school = postData['school'], study = postData['study'], city = postData['edu_city'], time_start = startEducation, time_end = endEducation, resume_id = postData['resume_id'])
                res['data'] = edu
        else:
            time1 = None
            time2 = None
            edu = Education.objects.create(degree = postData['degree'], school = postData['school'], study = postData['study'], city = postData['edu_city'], time_start = time1, time_end = time2, resume_id = postData['resume_id'])
            res['data'] = edu
        return res

    def edit_resume(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        if len(postData['skills']) < 1:
            res['status'] = "bad"
            res['data'] = "You must enter your skills!"
        else:
            resume = Resume.objects.get(id = postData['resume_id'])
            resume.about_self = postData['about_self']
            resume.desired_job = postData['desired_job']
            skill = Skill.objects.get(resume_id = resume.id)
            skill.skills = postData['skills']
            resume.save()
            skill.save()
        return res

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    banned = models.BooleanField(default = False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

class Address(models.Model):
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 45)
    state = models.CharField(max_length = 2)
    zip_code = models.SmallIntegerField(null = True)
    phone = models.IntegerField(null = True)
    user = models.OneToOneField(User)

    objects = AddressManager()

class Resume(models.Model):
    about_self = models.TextField(null = True)
    desired_job = models.TextField(null = True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.OneToOneField(User, blank = True, null = True)
    listings = models.ManyToManyField(Listing, related_name = "user_resumes")

    objects = ResumeManager()

class WorkExperience(models.Model):
    job_title = models.CharField(max_length = 255)
    company = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    time_start = models.DateField(null = True)
    time_end = models.DateField(null = True)
    description = models.TextField(blank = True)
    resume = models.ForeignKey(Resume, related_name = "experiences")

class Education(models.Model):
    degree = models.CharField(max_length = 255)
    school = models.CharField(max_length = 255)
    study = models.CharField(max_length = 255)
    city = models.CharField(max_length = 50)
    time_start = models.DateField(null = True, blank = True)
    time_end = models.DateField(null = True, blank = True)
    resume = models.ForeignKey(Resume, related_name = "educations")

class Skill(models.Model):
    skills = models.TextField(blank = True)
    resume = models.ForeignKey(Resume, related_name = "skills") 