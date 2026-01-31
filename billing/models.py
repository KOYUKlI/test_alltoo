from decimal import Decimal
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    expiration_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="product_price_gte_0"),
        ]

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
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )

    class Meta:
        unique_together = ("invoice", "product")
        constraints = [
            models.CheckConstraint(condition=Q(unit_price__gte=0), name="item_unit_price_gte_0"),
            models.CheckConstraint(condition=Q(quantity__gte=1), name="item_quantity_gte_1"),
        ]


    @property
    def line_total(self) -> Decimal:
        # total de la ligne = prix unitaire * quantité
        return self.unit_price * self.quantity
