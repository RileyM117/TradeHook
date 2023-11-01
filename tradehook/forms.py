from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

# Custom user creation form.
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1')

# Form for user to create a Customer Broker model object.
class CustomerBrokerForm(forms.ModelForm):
    class Meta:
        model = CustomerBrokers
        fields = ['broker_name', 'broker_api_key', 'broker_secret_key']
        
# Form for user to generate a TradeHook API Key
class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKeys
        fields = ['tradehook_api_key']

class APIKeyManagementForm(forms.Form):
    generate_api_key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'generate-button'}))
    delete_api_key = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'delete-button'}))