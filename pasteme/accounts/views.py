from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import user_passes_test


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')
    print(form.errors)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        #print(username)
        #print(password)
        user = authenticate(username=username, password=password)
        login(request, user)
        print(request, user.is_authenticated)
        if next:
            return redirect(next)
        return redirect("index_page")
    return render(request, 'accounts/login.html', {"form":form})



def registered_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = UserRegisterForm(request.POST or None)
    print(form.is_valid())
    if form.is_valid():
        print(form)
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=user.password)
        login(request,user)

        return redirect("index_page")
    return render(request, 'accounts/registered.html', {"form":form})

def logout_view(request):
    logout(request)
    return redirect('login_view')
