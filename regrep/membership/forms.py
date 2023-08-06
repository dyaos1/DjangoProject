from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from regrep.models import Member


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class RegisterMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["company", "department"]

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = Member
#         fields = (
#             "username",
#             "password",
#         )
