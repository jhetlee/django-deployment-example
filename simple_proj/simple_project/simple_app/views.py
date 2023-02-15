from django.shortcuts import render
from simple_app.forms import UserForm, UserProfileInfoForms

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout



# Create your views here.

def base(request):
    return render(request, 'simple_app/base.html')

def index(request):
    return render(request, 'simple_app/index.html')

def relative(request):
    return render(request, 'simple_app/relative.html')

def other(request):
    return render(request, 'simple_app/other.html')


def registration(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForms(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #save user_form to the databse
            user.set_password(user.password) # grab the password and hash it
            user.save() # save

            profile = profile_form.save(commit = False)
            profile.user = user # sets up one to one relation with user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForms()
    return render(request, 'simple_app/registration.html', {
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })

@login_required
def special(request):
    return HttpResponse("You are logged in, NICE!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("SOMEONE tried to login and failed!")
            print(f"Username:{username} and password: {password}")
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request,'simple_app/login.html')

