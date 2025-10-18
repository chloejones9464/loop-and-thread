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
        fields = (
            "default_display_name", "default_phone_number",
            "default_country", "default_postcode", "default_town_or_city",
            "default_street_address1", "default_street_address2",
            "default_county",
        )
        labels = {
            "default_display_name": "Display name",
            "default_phone_number": "Phone number",
            "default_country": "Country",
            "default_postcode": "Postal code",
            "default_town_or_city": "Town or city",
            "default_street_address1": "Street address 1",
            "default_street_address2": "Street address 2",
            "default_county": "County, state or local area",
        }
        widgets = {
            "default_display_name": forms.TextInput(
                attrs={"placeholder": "Display name"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        if self.user is not None:
            self.fields["email"].initial = self.user.email

    def save(self, commit=True):
        """
        Save Profile fields, and also persist the email to the related User.
        """
        profile = super().save(commit=False)

        if self.user is not None and "email" in self.cleaned_data:
            new_email = self.cleaned_data["email"]
            if new_email != self.user.email:
                self.user.email = new_email
                self.user.save(update_fields=["email"])

        if commit:
            profile.save()
        return profile

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email
