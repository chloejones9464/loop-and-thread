from django.urls import path
from .views import pattern_list, pattern_detail

urlpatterns = [
        path("", pattern_list, name="pattern_list"),
        path('<int:pk>/', pattern_detail, name='pattern_detail'),
    ]
