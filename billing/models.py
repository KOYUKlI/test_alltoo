from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    # Représente un produit vendable (ce qu'on ajoute à une facture)
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],  # empêche prix négatif
    )
    expiration_date = models.DateField(null=True, blank=True)  # peut être vide

    created_at = models.DateTimeField(auto_now_add=True)  # date de création auto
    updated_at = models.DateTimeField(auto_now=True)      # date de MAJ auto

    def __str__(self):
        return f"{self.name} ({self.price}€)"


class Invoice(models.Model):
    # Une facture : conteneur de plusieurs lignes (InvoiceItem)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.pk}"


class InvoiceItem(models.Model):
    # Une ligne de facture : 1 produit + quantité + prix unitaire figé (snapshot)
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",  # invoice.items.all()
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # empêche de supprimer un produit utilisé en facture
        related_name="invoice_items",
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]  # quantité >= 1
    )

    # Snapshot du prix au moment de l'ajout (la facture ne change pas si le produit change de prix après)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        # Interdit 2 lignes identiques (même produit) dans la même facture
        unique_together = ("invoice", "product")

    @property
    def line_total(self) -> Decimal:
        # total de la ligne = prix unitaire * quantité
        return self.unit_price * self.quantity
