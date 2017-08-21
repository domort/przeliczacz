from django.forms import ModelForm
from django import forms
from models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'carbo', 'protein', 'fat', 'cal', 'unit_weight',)
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text', 'required': 'required', 'class': 'pure-u-1-2'}),
            'protein': forms.TextInput(attrs={'type': 'number', 'required': 'required', 'step': 0.01, 'min': 0, 'class': 'pure-u-1-4'}),
            'fat': forms.TextInput(attrs={'type': 'number', 'required': 'required', 'step': 0.01, 'min': 0, 'class': 'pure-u-1-4'}),
            'carbo': forms.TextInput(attrs={'type': 'number', 'required': 'required', 'step': 0.01, 'min': 0, 'class': 'pure-u-1-4'}),
            'cal': forms.TextInput(attrs={'type': 'number', 'required': 'required', 'min': 0, 'class': 'pure-u-1-4'}),
            'unit_weight': forms.TextInput(attrs={'type': 'number', 'required': 'required', 'step': 0.1, 'min': 0, 'class': 'pure-u-1-4'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'pure-u-1-2'}),
        }
