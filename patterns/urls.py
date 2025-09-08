from django.urls import path
from . import views

app_name = "patterns"

urlpatterns = [
    path("", views.pattern_list, name="list"),
]
