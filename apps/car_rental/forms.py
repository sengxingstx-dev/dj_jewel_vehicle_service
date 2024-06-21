from django import forms
from .models import Car, Category, Rental, Payment


class CarForm(forms.ModelForm):
    car_image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Car
        fields = ['model', 'make', 'number_plate', 'price', 'category', 'car_image', 'available']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_slip']
