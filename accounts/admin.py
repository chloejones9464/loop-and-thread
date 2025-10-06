from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "default_display_name",
        "default_phone_number",
        "default_country",
        "default_town_or_city",
    )
    search_fields = (
        "user__username",
        "default_display_name",
        "user__email",
    )
    list_select_related = ("user",)
