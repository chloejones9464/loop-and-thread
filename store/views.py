from django.shortcuts import render
from patterns.models import Pattern


def home(request):
    latest_patterns = Pattern.objects.order_by("-created_at")[:8]
    return render(
                request,
                "store/home.html",
                {"latest_patterns": latest_patterns},
                )
