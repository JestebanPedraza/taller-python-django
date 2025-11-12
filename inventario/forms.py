from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """Formulario para el modelo Product."""

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción (opcional)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio en USD'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
 