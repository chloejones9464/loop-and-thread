from django.contrib import admin
from .models import Pattern, PatternCategory


@admin.register(PatternCategory)
class PatternCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "difficulty",
        "is_published",
        "created_at"
    )
    list_filter = ("is_published", "difficulty", "category")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
