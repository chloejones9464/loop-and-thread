# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile

@login_required
def account(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            instance=profile,
            user=request.user,
        )
        form.initial["user_id"] = request.user.pk

        if form.is_valid():
            new_email = form.cleaned_data["email"]
            if new_email and new_email != request.user.email:
                request.user.email = new_email
                request.user.save()

            form.save()

            messages.success(request, "Account updated.")
            return redirect("account")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)
        form.initial["user_id"] = request.user.pk

    return render(request, "account/account.html", {"form": form})
