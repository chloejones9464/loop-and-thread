from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from patterns.models import Pattern


def view_bag(request):

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """
    Add a pattern to the bag with qty locked to 1 (set-like behaviour).
    """
    redirect_url = request.POST.get("redirect_url") or "/"
    if request.method != "POST":
        return redirect(redirect_url)

    pattern = get_object_or_404(Pattern, pk=item_id)

    bag = request.session.get("bag", {})
    bag[str(item_id)] = True
    request.session["bag"] = bag

    messages.success(request, f"Added “{pattern.title}” to your bag.")
    return redirect(redirect_url)


def remove_from_bag(request, item_id):
    redirect_url = request.POST.get("redirect_url") or "/"
    bag = request.session.get("bag", {})
    bag.pop(str(item_id), None)
    request.session["bag"] = bag
    messages.info(request, "Item removed from your bag.")
    return redirect(redirect_url)
