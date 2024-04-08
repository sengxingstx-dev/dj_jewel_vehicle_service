from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Account
from apps.car_rental.models import Customer, RentalAgent


class RegistrationForm(UserCreationForm):
    # Add any additional fields or customizations you need
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=150, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email is already in use. Please use a different email.'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    # Form validations
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Incorrect username or password.')


class EditAgentProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = RentalAgent
        fields = ['profile_image', 'first_name', 'last_name', 'email', 'phone']


class EditCustomerProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Customer
        fields = ['profile_image', 'first_name', 'last_name', 'email', 'phone', 'address']
