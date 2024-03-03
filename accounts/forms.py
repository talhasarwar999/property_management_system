from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True)
    contact_number = forms.IntegerField(required=True)
    website = forms.CharField(max_length=255, required=False)
    address = forms.CharField(max_length=255, required=False)
    class Meta:
        model = User
        fields = ('company_name', 'contact_number', 'website', 'address','username', 'email', 'password1', 'password2')