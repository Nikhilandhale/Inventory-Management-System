from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Available_product_table


class ProductForm(forms.ModelForm):
    class Meta:
        model = Available_product_table
        fields = ['product_name', 'product_price', 'product_quantity']


class AddProductForm(forms.ModelForm):
    product_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Name'}))
    product_price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Price'}))
    product_quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity'}))

    class Meta():
        model = Available_product_table
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User  # Assuming you have imported User from django.contrib.auth.models
        fields = ['first_name', 'last_name', 'email']


class SearchForm(forms.Form):
    search_product = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Product Name', 'class': 'form-control my-0 py-1'}))
