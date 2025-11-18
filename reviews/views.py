from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from patterns.models import Pattern
from .models import Review
from .forms import ReviewForm


def _user_profile(request):
    if not request.user.is_authenticated:
        return None
    return getattr(request.user, "profile", None)


def _has_purchased(profile, pattern):
    from checkout.models import OrderLineItem
    return OrderLineItem.objects.filter(
        order__user_profile=profile,
        pattern=pattern
    ).exists()


@login_required
def create_review(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    profile = _user_profile(request)
    if not profile:
        messages.error(request, "You need a profile to leave a review.")
        return redirect("account")

    if not _has_purchased(profile, pattern):
        messages.warning(
            request,
            "Only customers who purchased this pattern can review it."
            )
        return redirect("pattern_detail", pk=pattern.id)

    if Review.objects.filter(pattern=pattern, user_profile=profile).exists():
        messages.info(
            request,
            "You’ve already reviewed this pattern."
            "You can edit your review instead.")
        return redirect(
            "edit_review",
            review_id=Review.objects.get(
                pattern=pattern,
                user_profile=profile).id
        )

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.pattern = pattern
            review.user_profile = profile
            review.mark_verified()
            review.save()
            messages.success(request, "Thanks for your review! 🧶")
            return redirect("pattern_detail", pk=pattern.id)
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/review_form.html",
        {"form": form, "pattern": pattern}
        )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    profile = _user_profile(request)
    if review.user_profile != profile:
        messages.error(request, "You can only edit your own review.")
        return redirect("pattern_detail", pk=review.pattern.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.mark_verified()
            review.save()
            messages.success(request, "Your review was updated.")
            return redirect("pattern_detail", pk=review.pattern.id)
        messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/review_form.html",
        {"form": form, "pattern": review.pattern, "is_edit": True}
        )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    profile = _user_profile(request)
    if review.user_profile != profile:
        messages.error(request, "You can only delete your own review.")
        return redirect("pattern_detail", pk=review.pattern.id)

    if request.method == "POST":
        pattern_id = review.pattern.id
        review.delete()
        messages.success(request, "Your review was deleted.")
        return redirect("pattern_detail", pk=pattern_id)

    return render(
        request,
        "reviews/review_confirm_delete.html",
        {"review": review}
        )
