from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'label',
            'description',
            'price',
            'stock',
            'category',
            'image1',
            'image2',
            'image3',
            'image4',
        ]