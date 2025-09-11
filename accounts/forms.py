from django import forms
from crispy_forms.helper import FormHelper
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("display_name",)
        widgets = {
            "display_name": forms.TextInput(
                attrs={"placeholder": "Public name"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Let the outer template control the <form> tag
        self.helper = FormHelper()
        self.helper.form_tag = False
