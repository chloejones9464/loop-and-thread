from django.urls import path
from .views import pattern_list

urlpatterns = [
        path("", pattern_list, name="pattern_list"),
    ]
