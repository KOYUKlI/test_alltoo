from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, formset_factory

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


class InvoiceLineForm(forms.Form):
    # Une "ligne" de facture côté formulaire : produit + quantité
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,  # on autorise vide, la validation globale gère le minimum 1 ligne
    )
    quantity = forms.IntegerField(
        min_value=1,
        required=False,  # idem, peut être vide tant qu'au moins une ligne est remplie
    )


class RequiredInvoiceLineFormSet(BaseFormSet):
    def clean(self):
        """
        Vérifie qu'il y a au moins 1 ligne valide (produit + quantité).
        Ça évite de créer une facture vide.
        """
        super().clean()

        valid_lines = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE"):
                continue

            product = form.cleaned_data.get("product")
            quantity = form.cleaned_data.get("quantity")
            if product and quantity:
                valid_lines += 1

        if valid_lines < 1:
            raise ValidationError("Ajoutez au moins un produit à la facture.")


# Pour l’instant : 5 lignes par défaut (on mettra le bouton JS au commit suivant)
InvoiceLineFormSet = formset_factory(
    InvoiceLineForm,
    formset=RequiredInvoiceLineFormSet,
    extra=5,
    can_delete=True,
)
