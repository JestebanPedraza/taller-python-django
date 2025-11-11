from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """Formulario para el modelo Product."""

    class Meta:
        model = Product
        fields = '__all__'
 