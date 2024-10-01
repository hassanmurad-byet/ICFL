from django import forms
from .models import Profile


class ProfilePic(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pro_pic']

