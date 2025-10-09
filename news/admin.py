from django.contrib import admin
from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "publish_at",
        "created_by",
        "updated_at",
    )
    list_filter = ("status", "publish_at")
    search_fields = ("title", "summary", "body")
    date_hierarchy = "publish_at"
    readonly_fields = ("created_at", "updated_at")
