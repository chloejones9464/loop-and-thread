from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "title", "body")
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "title": forms.TextInput(attrs={"placeholder": "Optional title"}),
            "body": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Share your thoughts…"}
            ),
        }
