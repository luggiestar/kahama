from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
import json

from ..models import *


def home(request):
    return render(request, 'KCHS/home.html')


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if request.user.is_superuser:

                    return redirect("admin:index")
                else:
                    return redirect('KCHS:user_home')

        else:
            # messages.error(request, f"Invalid username or password. please make sure you enter valid credentials")
            messages.success(request, 'Invalid username or password')
            return redirect('KCHS:login')

    return render(request, 'KCHS/login.html')


def user_home(request):
    get_user = get_object_or_404(User, id=request.user.id)
    try:
        get_student=get_object_or_404(Registration, student__user=get_user)
    except:
        get_student=None
    context = {
        'user': get_student,
    }
    return render(request, 'KCHS/user_home.html', context)
