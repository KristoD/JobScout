from __future__ import unicode_literals
from django.db import models
from ..users.models import *
import bcrypt
import stripe
from job_scout import settings
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
stripe.api_key = settings.STRIPE_SECRET_KEY

class EmployerManager(models.Manager):
    def registration_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['company']) < 1:
            errors.append("Must enter a Company name!")
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
        if len(Employer.objects.filter(email = postData['email'])):
            errors.append("Email is already in use.")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            employer = Employer.objects.create(company_name = postData['company'], first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed_pw)
            res['data'] = employer
        return res

    def login_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        try:
            the_employer = Employer.objects.get(email = postData['email'])
        except:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res
        if the_employer.banned == True:
            res['status'] = "bad"
            res['data'] = "Sorry pal. You've been banned. If you feel this was a mistake, send us an email. You probably will never get a response."
            return res
        if bcrypt.checkpw(postData['password'].encode(), the_employer.password.encode()):
            res['data'] = the_employer
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
        employer = Employer.objects.get(id = postData['employer_id'])
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append("First and last name should be more than 2 characters.")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors.append("First and last name can only contain alphabetic characters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be in correct format.")
        if postData['email'] != employer.email:
            if len(Employer.objects.filter(email = postData['email'])):
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
            if postData['password'] != "" and postData['email'] != employer.email:
                hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
                employer.first_name = postData['first_name']
                employer.last_name = postData['last_name']
                employer.email = postData['email']
                employer.password = hashed_pw
                employer.save()
            elif postData['email'] != employer.email:
                employer.first_name = postData['first_name']
                employer.last_name = postData['last_name']
                employer.email = postData['email']
                employer.save()
            else:
                employer.first_name = postData['first_name']
                employer.last_name = postData['last_name']
                employer.save()
            res['data'] = employer
        return res

class EmployerAddressManager(models.Manager):
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
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            address = EmployerAddress.objects.create(address = postData['address'], city = postData['city'], zip_code = postData['zip_code'], phone = postData['phone'], employer_id = postData['company_id'])
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
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            address = EmployerAddress.objects.get(employer_id = postData['employer_id'])
            address.address = postData['address']
            address.city = postData['city']
            address.zip_code = postData['zip_code']
            address.phone = postData['phone']
            address.save()
            res['data'] = address
        return res

class ListingManager(models.Manager):
    def listing_validator(self, postData):
        new_listing = Listing(title = postData['title'], company_description = postData['company_desc'], job_description = postData['job_desc'], city = postData['city'], employer_id = postData['employer_id'])
        token = postData["stripeToken"]
        try:
            charge = stripe.Charge.create(
                amount = 5000,
                currency = "usd",
                source = token,
                description = "The product charged to the user")
            new_listing.charge_id = charge.id
        except stripe.error.CardError as ce:
            return False, ce
        else:
            new_listing.save()
            ConfirmListing.objects.get(id = postData['confirm_id']).delete()
            return new_listing

    def edit_listing(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['title']) < 1:
            errors.append("Must enter a title!")
        if len(postData['company_desc']) < 1:
            errors.append("Must enter a company description!")
        if len(postData['job_desc']) < 1:
            errors.append("Must enter a job description!")
        if len(postData['city']) < 1:
            errors.append("Must enter a city!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            listing = Listing.objects.get(id = postData['listing_id'])
            listing.title = postData['title']
            listing.company_description = postData['company_desc']
            listing.job_description = postData['job_desc']
            listing.city = postData['city']
            listing.state = postData['state']
            listing.save()
            res['data'] = listing
        return res

class ConfirmListingManager(models.Manager):
    def confirmation(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['title']) < 1:
            errors.append("Must enter a title!")
        if len(postData['company_desc']) < 1:
            errors.append("Must enter a company description!")
        if len(postData['job_desc']) < 1:
            errors.append("Must enter a job description!")
        if len(postData['city']) < 1:
            errors.append("Must enter a city!")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            confirm_listing = ConfirmListing.objects.create(title = postData['title'], company_description = postData['company_desc'], job_description = postData['job_desc'], city = postData['city'], employer = postData['employer_id'])
            res['data'] = confirm_listing
        return res


class Employer(models.Model):
    company_name = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    banned = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployerManager()

class EmployerAddress(models.Model):
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    zip_code = models.SmallIntegerField(null = True)
    phone = models.IntegerField(null = True)
    employer = models.OneToOneField(Employer)

    objects = EmployerAddressManager()

class Listing(models.Model):
    title = models.CharField(max_length = 255)
    company_description = models.TextField(blank = True)   
    job_description = models.TextField(blank = True)
    city = models.CharField(max_length = 45)
    charge_id = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employer = models.ForeignKey(Employer, related_name = "listings")
    
    objects = ListingManager()

class ConfirmListing(models.Model):
    title = models.CharField(max_length = 255)
    company_description = models.TextField(blank = True)   
    job_description = models.TextField(blank = True)
    city = models.CharField(max_length = 45)
    employer = models.SmallIntegerField(null = True)

    objects = ConfirmListingManager()