# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from .models import Profile
from checkout.models import Order


@login_required
def account(request):
    profile, _ = Profile.objects.get_or_create(default_user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST or None,
            instance=profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated.")
            return redirect("account")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "account/account.html", {"form": form})


@login_required
def orders_list(request):
    profile = request.user.profile
    orders = (
        profile.orders
        .select_related("user_profile")
        .prefetch_related("lineitems__pattern")
        .order_by("-date")
    )
    return render(request, "account/orders_list.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    profile = request.user.profile
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile=profile
    )
    return render(request, "account/order_details.html", {"order": order})