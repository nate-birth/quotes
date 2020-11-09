from django.db import models
from datetime import datetime, timedelta, tzinfo
import re

class UserManager(models.Manager):
    def validator(self, postdata):
        errors = {}
        email_chex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['f_n']) < 2:
            errors['f_n'] = "First name must be longer than 2 Characters"
        if len(postdata['l_n']) < 2:
            errors['l_n'] = "Last name must be longer than 2 Characters"
        if not email_chex.match(postdata['email']):
            errors['email'] = "Invalid Email Address"
        if len(postdata['pw']) < 8:
            errors['pw'] = "Password must be longer than 8 Characters"
        if postdata['pw'] != postdata['c_pw']:
            errors['c_pw'] = "Password must match"
        if self.filter(email=postdata['email']).exists():
            errors['reg'] = "Email already in use"
        return errors

    def updateValidator(self, postdata):
        errors = {}
        email_chex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        copy_chex = self.get(id=postdata['id'])
        if len(postdata['f_n']) < 2:
            errors['f_n'] = "First name must be longer than 2 Characters"
        if len(postdata['l_n']) < 2:
            errors['l_n'] = "Last name must be longer than 2 Characters"
        if not email_chex.match(postdata['email']):
            errors['email'] = "Invalid Email Address"
        if copy_chex.email != postdata['email']:
            if self.filter(email=postdata['email']).exists():
                errors['used'] = "Email already in use"
        return errors

        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class QuoteManager(models.Manager):
    def validator(self, postdata):
        errors = {}
        if len(postdata['author']) < 4:
            errors['author'] = "Author name must be longer than 3 characters."
        if len(postdata['quote']) < 11:
            errors['quote'] = "Quote must be more than 10 characters."
        return errors

class Quotes(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey(User, related_name="quotes_posted", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
