from django import forms
from .models import Pattern


class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = [
            "title", "category", "summary", "description",
            "difficulty", "price", "cover_image", "file", "is_published"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "summary": forms.Textarea(attrs={"rows": 2}),
        }
