from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.forms import ProfileModelForm, UserModelForm


@login_required
def v_logout_view(request):
    logout(request)
    return redirect("accounts:login")


def v_profile(request):
    context = {"user": User.objects.get(id=request.user.id)}
    return render(request, "registration/profile.html", context)


def v_profile_edit(request):
    o_user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = ProfileModelForm(request.POST, instance=o_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved Successfully")
            return redirect("accounts:profile")
        else:
            for field, err in form.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )
    context = {"user": o_user}
    return render(request, "registration/profile_edit.html", context)


def v_signup_view(request):
    if request.method == "POST":
        request.POST = request.POST.copy()
        request.POST["username"] = request.POST["email"].split("@")[0]
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved Successfully")
            return redirect("accounts:login")
        else:
            for field, err in form.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )

    context = {"form": UserModelForm()}
    return render(request, "registration/signup.html", context)
