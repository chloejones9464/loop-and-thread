from django.urls import path
from .views import pattern_list, pattern_detail
from . import views

urlpatterns = [
        path("", pattern_list, name="pattern_list"),
        path('<int:pk>/', pattern_detail, name='pattern_detail'),
        path("manage/", views.manage_patterns, name="patterns_manage"),
        path("add/", views.add_pattern, name="pattern_add"),
        path("<int:pk>/edit/", views.edit_pattern, name="pattern_edit"),
        path(
            "favourites/toggle/<int:pattern_id>/",
            views.toggle_favourite,
            name="toggle_favourite"
        ),
        path("favourites/", views.my_favourites, name="my_favourites"),
    ]
