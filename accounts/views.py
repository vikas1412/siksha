

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        messages.success(request,
                         "You are already logged in to your account. If however, you want to log in from another "
                         "account, you must log out of this account first.")
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            current_user = authenticate(username=username, password=password)
            if current_user is not None:
                login_auth(request, current_user)

                if request.user.is_staff:
                    messages.success(request, "Welcome back to QComp. Now you can add new Quiz for your students and"
                                              "check status.")
                    # return redirect('dashboard')
                    return redirect('home')
                else:
                    messages.success(request, "Welcome back to QComp. Now you can attempt Quiz for your practice.")
                    return redirect('home')
            else:
                messages.error(request,
                               'Invalid username or password. Make sure that you enter a correct username or '
                               'password. In case you forget it, please reset your password')
                return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "GET":
        logout_auth(request)
        request.session.flush()
        messages.warning(
            request, "You have successfully been logged out of your account.")
        return redirect('home')
    return render(request, 'create_exam/home.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['username']
        pass1 = request.POST['pass1']

        try:
            user = User.objects.get(username=username)
            messages.warning(request, "User already exist with the username you enetered.")
            redirect('signup')
        except User.DoesNotExist:
            new_user = User.objects.create_user(username, email, pass1)
            new_user.first_name = first_name
            new_user.last_name = last_name

            curr_user = authenticate(username=username, password=pass1)
            if curr_user is not None:
                login_auth(request, curr_user)
            messages.success(
                request, f"Welcome to QComp. {first_name} {last_name}. Now you can take quiz.")
            return redirect('home')

    return render(request, 'accounts/signup.html')
