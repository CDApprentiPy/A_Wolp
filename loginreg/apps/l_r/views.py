# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User
import bcrypt

# Create your views here.


def index(request):
    return render(request, "l_r/index.html")


def process(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('main'))
        else:
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            print password          
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password,)
            user = User.objects.last()
            request.session['user_id'] = user.id
            request.session['status'] = "new"            
            return redirect('success')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('main'))
        else:
            user = User.objects.get(email=request.POST['username'])
            request.session['user_id'] = user.id
            request.session['status'] = "active"
            return redirect('success')
    return redirect(reverse('success'))


def success(request):
    id = request.session['user_id']
    status = request.session['status']
    if status == "active":
        text = "Welcome back"
    else:
        text = "Thanks for signing up"
    context = {
        "first_name" : User.objects.get(id=id).first_name,
        "message" : text
    }
    return render(request, "l_r/success.html", context)

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect(reverse('main'))
        