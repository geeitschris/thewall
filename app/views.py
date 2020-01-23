from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def createuser(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return render(request, 'index.html')
    password = request.POST['password']
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
    request.session['userid'] = new_user.id
    return redirect('/success')


def dashboard(request):
    if request.session.get('userid') is None:
        return redirect('/')
    user = User.objects.filter(id=request.session['userid'])
    context = {
        "user": user[0],
        "message": Post.objects.all()
    }
    return render(request, "dashboard.html", context)


def login(request):
    errors = {}
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(request.POST['email']) == "" or not EMAIL_REGEX.match(request.POST['email']):
        errors['email'] = 'Invalid E-Mail'
    if len(request.POST['password']) < 8:
        errors['password'] = 'Password must be at least 8 characters'
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')
    for k, v in errors.items():
        messages.error(request, v)
    return render(request, 'index.html')


def logout(request):
    request.session.clear()
    return redirect('/')


def post(request):
    if request.session.get('userid') is None:
        return redirect('/')
    user_from_db = User.objects.get(id=request.session['userid'])
    message = Post.objects.create(
        content=request.POST['message'], author=user_from_db)
    return redirect('/success')


def comment(request, messageid):
    if request.session.get('userid') is None:
        return redirect('/')
    user_from_db = User.objects.get(id=request.session['userid'])
    comment = Comment.objects.create(
        content=request.POST['comment'], message=Post.objects.get(id=messageid), author=user_from_db)
    return redirect('/success')
