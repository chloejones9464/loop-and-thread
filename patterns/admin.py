from django.contrib import admin
from .models import Pattern, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Pattern, PatternAdmin)
