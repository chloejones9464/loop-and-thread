from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Pattern, Favorite
from django.http import JsonResponse
from .forms import PatternForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def pattern_list(request):
    qs = Pattern.objects.all()

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user)
                            .values_list("pattern_id", flat=True)
        )

    query = request.GET.get("q", "").strip()

    if "q" in request.GET:
        if not query:
            messages.error(request, "You didn't enter anything to search")
            return redirect("pattern_list")

        qs = qs.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    sort = request.GET.get("sort", "")
    direction = request.GET.get("direction", "")

    if sort in ["price", "title", "created_at"]:
        if direction == "desc":
            sortkey = f"-{sort}"
        else:
            sortkey = sort
        qs = qs.order_by(sortkey)

    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "patterns/pattern_list.html",
        {

            "page_obj": page_obj,
            "patterns": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "search_term": query,
            "favorite_ids": favorite_ids,
        },
    )


def pattern_detail(request, pk):
    pattern = get_object_or_404(Pattern, pk=pk)
    return render(
                request,
                "patterns/pattern_detail.html",
                {"pattern": pattern},
                )


def _superuser_only(request):
    if not request.user.is_authenticated:
        return False
    return request.user.is_superuser


@login_required
def manage_patterns(request):
    if not _superuser_only(request):
        messages.error(request, "Sorry, only site owners can manage patterns.")
        return redirect("home")
    patterns = Pattern.objects.all().order_by("-id")
    return render(
        request,
        "patterns/manage_patterns.html",
        {"patterns": patterns}
    )


@login_required
def add_pattern(request):
    if not _superuser_only(request):
        messages.error(request, "Sorry, only site owners can add patterns.")
        return redirect("home")

    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES)
        if form.is_valid():
            pattern = form.save()
            messages.success(request, f'Pattern "{pattern.title}" created.')
            return redirect("patterns_manage")
        messages.error(request, "Please fix the errors below.")
    else:
        form = PatternForm()

    return render(
        request,
        "patterns/pattern_form.html",
        {
            "form": form,
            "mode": "add"
        }
    )


@login_required
def edit_pattern(request, pk):
    if not _superuser_only(request):
        messages.error(request, "Sorry, only site owners can edit patterns.")
        return redirect("home")

    pattern = get_object_or_404(Pattern, pk=pk)

    if request.method == "POST":
        form = PatternForm(request.POST, request.FILES, instance=pattern)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pattern "{pattern.title}" updated.')
            return redirect("patterns_manage")
        messages.error(request, "Please fix the errors below.")
    else:
        form = PatternForm(instance=pattern)

    return render(
        request, "patterns/pattern_form.html",
        {"form": form, "mode": "edit", "pattern": pattern}
    )


@login_required
def delete_pattern(request, pk):
    if not _superuser_only(request):
        messages.error(request, "Sorry, only site owners can delete patterns.")
        return redirect("home")

    pattern = get_object_or_404(Pattern, pk=pk)

    if request.method == "POST":
        title = pattern.title
        pattern.delete()
        messages.success(request, f'Pattern "{title}" deleted.')
        return redirect("patterns_manage")

    return render(
        request,
        "patterns/pattern_confirm_delete.html",
        {"pattern": pattern}
    )


@login_required
@require_POST
def toggle_favorite(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    fav, created = Favorite.objects.get_or_create(
        user=request.user, pattern=pattern
    )

    if created:
        messages.success(request, "Added to favorites.")
        favorited = True
    else:
        fav.delete()
        messages.success(request, "Removed from favorites.")
        favorited = False

    count = Favorite.objects.filter(pattern=pattern).count()

    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return redirect(request.POST.get("next") or "/")

    return JsonResponse({"ok": True, "favorited": favorited, "count": count})


@login_required
def my_favorites(request):
    items = (
        Favorite.objects
        .filter(user=request.user)
        .select_related("pattern")
        .order_by("-created_at")
    )
    return render(request, "patterns/my_favorites.html", {"items": items})
