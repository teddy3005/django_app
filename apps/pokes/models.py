from __future__ import unicode_literals
import re
from datetime import date, datetime
from django.db import models 
import bcrypt
regex=re.compile(r'^[a-zA-Z0-9]+$')

class usermanager(models.Manager):
    def validation(self,postData):
        errors = {}
        if len(postData['name']) <  3:
            errors['name'] = "Name should be no fewer than 3 characters"
        if any(char.isdigit() for char in postData['name']) == True:
            errors['name'] = "Name can not have numbers"
        if len(postData['username']) <  3:
            errors['username'] = "Username should be no fewer than 3 characters"
        if not regex.match(postData['password']):
            errors['password'] = "Password can not have special characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be greater than 8 characters"
        
        if postData['confirmpassword'] !=postData['password']:
            errors['confirmpassword'] = "Passwords do not match"
        if len(postData['birthday'])==0 or datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
            errors['birthday'] = "please enter a birthday"
        
        if len(User.objects.filter(username=postData["username"])) > 0:
            errors["username"] = "username already exist"
        if len(errors)==0:
            bcryptpassword = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            currentuser=User.objects.create(name=postData['name'],username=postData['username'],birthday=postData['birthday'],password=bcryptpassword)
            errors['user']=currentuser
        return errors

    def loginvalidation(self,postData):
        errors={}
        checklogin= User.objects.filter(username=postData["username"])
        if checklogin:
            if bcrypt.checkpw(postData['password'].encode(),checklogin[0].password.encode()) == True:
                errors["user"]=checklogin[0]
            else:
                errors['password']= "Log in Failed"
        else:
            errors['username']= "Log in Failed"
        return errors
   
class User(models.Model):
    name=models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthday = models.DateField()
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=usermanager()

class Pokes(models.Model):
    sender = models.ForeignKey(User, related_name="senderspoke")
    receiver = models.ForeignKey(User, related_name ="receiverspoke")
    pokes = models.IntegerField(null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)