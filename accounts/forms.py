# profiles/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )

    class Meta:
        model = Profile
        fields = ("display_name",)
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Username"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        
        if user is not None:
            self.fields["email"].initial = user.email

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        
        if User.objects.filter(email__iexact=email).exclude(
            pk=self.initial.get("user_id")
        ).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
