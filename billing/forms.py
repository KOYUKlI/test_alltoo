from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # Formulaire simple pour créer/modifier un produit
    class Meta:
        model = Product
        fields = ["name", "price", "expiration_date"]
        widgets = {
            # permet d'avoir un sélecteur de date dans le navigateur
            "expiration_date": forms.DateInput(attrs={"type": "date"})
        }
