from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "middle_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "middle_name", "last_name", "role")


class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ["first_name", "middle_name", "last_name", "profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_image"].widget.attrs.update({"class": "form-control-file"})
