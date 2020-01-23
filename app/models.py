from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name']) < 2:
            errors['first_name'] = 'First name should contain at least 2 characters'
        if len(data['last_name']) < 2:
            errors['last_name'] = 'Last name should contain at least 3 characters'
        if len(data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if data['password'] != data['cpassword']:
            errors['password'] = 'Passwords do not match'
        if len(data['email']) == "" or not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Invalid E-Mail'
        pw = User.objects.filter(email=data['email'])
        if len(pw) > 0:
            errors['email'] = 'Invalid Credentials'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.content} {self.author}'


class Comment(models.Model):
    content = models.TextField()
    message = models.ForeignKey(
        Post, related_name='message', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
