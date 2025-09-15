from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile


@login_required
def account(request):
    account, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated.")
            return redirect("account")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=account)

    return render(request, "account/account.html", {"form": form})
