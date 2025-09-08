from django.shortcuts import render
from django.http import HttpResponse


def pattern_list(request):
    return HttpResponse("Patterns list works!")
