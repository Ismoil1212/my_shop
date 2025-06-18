from ast import If
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


from users.forms import (
    UserLoginForm,
    UserProfileForm,
    UserRegistrationForm,
)


def registration(request):

    if request.method == "POST":

        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(
                request,
                f"{user.username}, you have successfully registered and logged into your account",
            )
            return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserRegistrationForm()

    context = {
        "title": "Home - registration",
        "form": form,
    }

    return render(request, "users/registration.html", context)


def login(request):

    if request.method == "POST":

        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(
                    request,
                    f"{user.username}, you have successfully logged into your account",
                )

                if request.POST.get("next", None):
                    return HttpResponseRedirect(request.POST.get("next"))

                return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserLoginForm()

    context = {
        "title": "Home - login",
        "form": form,
    }

    return render(request, "users/login.html", context)


@login_required
def profile(request):

    if request.method == "POST":

        form = UserProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile was successfully updated",
            )

            return HttpResponseRedirect(reverse("user:profile"))

    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "title": "Home - Profile",
        "form": form,
    }

    return render(request, "users/profile.html", context)


def users_cart(request):
    return render(request, "users/users_cart.html")


@login_required
def logout(request):
    auth.logout(request)
    messages.success(
        request,
        f"You have logout from your account",
    )
    return redirect(reverse("main:index"))
