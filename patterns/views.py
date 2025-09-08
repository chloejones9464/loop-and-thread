from django.shortcuts import render, get_object_or_404
from .models import Pattern


def pattern_list(request):
    patterns = Pattern.objects.all().order_by("-id")
    return render(request, "patterns/pattern_list.html", {"patterns": patterns})


# def pattern_detail(request, slug):
#     pattern = get_object_or_404(Pattern, slug=slug)
#     return render(request, "patterns/pattern_detail.html", {"pattern": pattern})
