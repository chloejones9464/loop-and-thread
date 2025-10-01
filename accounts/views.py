# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile


@login_required
def account(request):
    profile, _ = Profile.objects.get_or_create(default_user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST or None, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated.")
            return redirect("account")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "account/account.html", {"form": form})