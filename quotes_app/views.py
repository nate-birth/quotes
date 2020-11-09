from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        pword = request.POST['pw']
        hashword = bcrypt.hashpw(pword.encode(), bcrypt.gensalt()).decode()
        print(hashword)
        reg_user = User.objects.create(
            first_name=request.POST['f_n'],
            last_name=request.POST['l_n'],
            email=request.POST['email'],
            password=hashword)
        print(reg_user)
        request.session['uid'] = reg_user.id
        request.session['uname'] = reg_user.full_name
        return redirect('/quotes')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['uid'] = logged_user.id
                request.session['uname'] = logged_user.full_name
                return redirect('/quotes')
    messages.error(request, "Email or Password is not Valid.")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def profile(request, u_id):
    if 'uid' not in request.session or request.session['uid'] != u_id:
        return redirect('/')
    context = {
        'user': User.objects.get(id=u_id)
    }
    return render(request, 'profile.html', context)

def update(request, u_id):
    if request.method == 'POST':
        errors = User.objects.updateValidator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/myaccount/{u_id}')
        user = User.objects.get(id=u_id)
        user.first_name = request.POST['f_n']
        user.last_name = request.POST['l_n']
        user.email = request.POST['email']
        user.save()
        messages.success(request, "Updated!")
    return redirect(f'/myaccount/{u_id}')

def quotes(request):
    if 'uid' not in request.session:
        return redirect('/')
    context = {
        'all_quotes': Quotes.objects.all(),
        'curr_user': User.objects.get(id=request.session['uid'])
    }
    return render(request, 'quotes.html', context)

def user_quotes(request, u_id):
    if 'uid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=u_id)
    }
    return render(request, 'user_posts.html', context)

def add(request):
    if request.method == 'POST':
        errors = Quotes.objects.validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
        user = User.objects.get(id=request.POST['user'])
        new_quote = Quotes.objects.create(
            author=request.POST['author'],
            content=request.POST['quote'],
            posted_by=user)
        new_quote.liked_by.add(user)
    return redirect('/quotes')

def delete(request, q_id):
    if 'uid' not in request.session:
        return redirect('/')
    quote = Quotes.objects.get(id=q_id)
    quote.delete()
    return redirect('/quotes')

def like(request, q_id):
    if 'uid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['uid'])
    quote = Quotes.objects.get(id=q_id)
    user.liked_quotes.add(quote)
    return redirect('/quotes')