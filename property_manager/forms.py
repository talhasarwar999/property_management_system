from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Property
from tanant.models import Tanant
User = get_user_model()


class ProfileUpdateForm(UserChangeForm):
    company_name = forms.CharField(max_length=255, required=True)
    contact_number = forms.IntegerField(required=True)
    website = forms.CharField(max_length=255, required=False)
    address = forms.CharField(max_length=255, required=False)
    logo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('company_name', 'contact_number', 'website', 'address','username', 'email', 'logo',)


class CustomPasswordChangeForm(PasswordChangeForm):
    pass


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['owner', 'images', 'documents']


class TanantForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Tanant
        fields = '__all__'
        exclude = ['user', 'images']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(TanantForm, self).__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False