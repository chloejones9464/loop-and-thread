from django.urls import path
from .views import pattern_list, pattern_detail
from . import views

urlpatterns = [
        path("", pattern_list, name="pattern_list"),
        path('<int:pk>/', pattern_detail, name='pattern_detail'),
        path("manage/", views.manage_patterns, name="patterns_manage"),
        path("add/", views.add_pattern, name="pattern_add"),
        path("<int:pk>/edit/", views.edit_pattern, name="pattern_edit"),
        path("<int:pk>/delete/", views.delete_pattern, name="pattern_delete"),
        path(
            "favorites/toggle/<int:pattern_id>/",
            views.toggle_favorite,
            name="toggle_favorite"
        ),
        path("favorites/", views.my_favorites, name="my_favorites"),
    ]
