# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        a=User.objects.filter(email=postData['email'])
        for k, v in postData.items():
            if len(v) < 1:
                errors["empty"] = "Please complete all fields"
                return errors
        if len(a) > 0:
            errors["active"] = "You've already registered, please log in"  
            return errors          
        if len(postData["first_name"])  < 2 or len(postData["last_name"]) < 2:
            errors["name_len"] = "Name needs to be longer than 2 letters"
        if any(i.isalpha() is False for i in postData['first_name']):
            errors["digits"] = "Name can only contain letters "
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Please enter a valid email address "
        if len(postData['password']) < 8:
            errors["password_len"] = "Password must be longer than 8 characters"
        if postData['password'] != postData['cpwd']:
            errors["cpwd_comf"] = "Passwords do not match"
            
        return errors
        
    def login_validator(self, postData):
        errors = {}
        email = postData['username']
        password = postData['pword'].encode()
        try:
            a = User.objects.get(email=email)
        except User.DoesNotExist:
            errors["reg"] = "Please register first"
            return errors
        if bcrypt.checkpw(password.encode(), a.password.encode()) is False:
            errors["incorrect"] = "Incorrect password!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)   
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()