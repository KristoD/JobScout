from __future__ import unicode_literals
from django.db import models
import bcrypt

class AdminManager(models.Manager):
    def create_validator(self, postData):
        pass

    def login_validator(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        try:
            admin = Admin.objects.get(email = postData['email'])
        except:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res
        # if bcrypt.checkpw(postData['password'].encode(), admin.password.encode()):
        if postData['password'] == admin.password:
            res['data'] = admin
            return res
        else:
            res['status'] = "bad"
            res['data'] = "Email or Password incorrect"
            return res

class Admin(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = AdminManager()
