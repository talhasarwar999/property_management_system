from django.contrib.auth import get_user_model
from django import forms
from .models import Tanant
User = get_user_model()

class TanantForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Tanant
        fields = '__all__'
        exclude = ['user', 'files']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(TanantForm, self).__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False