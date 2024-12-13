from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserModelForm


@login_required
def v_homepage(request):
    return redirect("invoices:dashboard")


@login_required
def v_logout_view(request):
    logout(request)
    return redirect("accounts:login")


def v_profile(request):
    context = {"user": User.objects.get(id=request.user.id)}
    return render(request, "registration/profile.html", context)


def v_signup_view(request):
    if request.method == "POST":
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    context = {"form": UserModelForm()}
    return render(request, "registration/signup.html", context)
