from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1')

class CustomerBrokerForm(forms.ModelForm):
    class Meta:
        model = CustomerBrokers
        fields = ['broker_name', 'broker_api_key', 'broker_secret_key']

class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKeys
        fields = ['tradehook_api_key']

class APIKeyManagementForm(forms.Form):
    generate_api_key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'generate-button'}))
    delete_api_key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'delete-button'}))