from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Pattern
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


def pattern_list(request):
    qs = Pattern.objects.order_by("-id")

    query = request.GET.get("q", "").strip()

    if "q" in request.GET:
        if not query:
            messages.error(request, "You didn't enter anything to search")
            return redirect("pattern_list")

        qs = qs.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(qs, 6)
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
        },
    )


def pattern_detail(request, pk):
    pattern = get_object_or_404(Pattern, pk=pk)
    return render(
                request,
                "patterns/pattern_detail.html",
                {"pattern": pattern},
                )
