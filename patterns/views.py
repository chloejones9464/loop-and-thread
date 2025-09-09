from django.shortcuts import render, get_object_or_404
from .models import Pattern
from django.core.paginator import Paginator


def pattern_list(request):
    patterns = Pattern.objects.all().order_by("-id")
    paginator = Paginator(patterns, 6)  # 6 per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
                request,
                "patterns/pattern_list.html",
                {
                    "patterns": page_obj,
                    'page_obj': page_obj,
                    'is_paginated': page_obj.has_other_pages(),
                },
            )


def pattern_detail(request, pk):
    pattern = get_object_or_404(Pattern, pk=pk)
    return render(
                request,
                "patterns/pattern_detail.html",
                {"pattern": pattern},
                )
