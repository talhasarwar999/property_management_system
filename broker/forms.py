from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Broker
User = get_user_model()

class BrokerForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Broker
        fields = '__all__'
        exclude = ['user', 'files']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(BrokerForm, self).__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False


class BrokerProfileUpdateForm(UserChangeForm):
    company_name = forms.CharField(max_length=255, required=True)
    contact_number = forms.IntegerField(required=True)
    city = forms.CharField(max_length=255, required=False)
    address = forms.CharField(max_length=255, required=False)
    logo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('company_name', 'contact_number', 'city', 'address','username', 'email', 'logo',)